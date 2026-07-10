import json
import os
import re
import urllib.request
import boto3
import pymysql
from datetime import datetime

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")
DB_HOST = os.environ.get("DB_HOST", "").split(":")[0]
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")


def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )


def get_active_incident():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM incidents WHERE status = '발생중' ORDER BY started_at DESC LIMIT 1"
            )
            return cursor.fetchone()
    except Exception as e:
        print(f"RDS 조회 실패: {e}")
        return None
    finally:
        conn.close()


def update_incident_resolved(incident_id, ended_at, downtime):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE incidents SET status='종료', ended_at=%s, downtime=%s WHERE id=%s",
                (ended_at, downtime, incident_id)
            )
        conn.commit()
    except Exception as e:
        print(f"RDS 업데이트 실패: {e}")
    finally:
        conn.close()


def send_slack_message(channel, text):
    data = json.dumps({
        "channel": channel,
        "text": text
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
        }
    )
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))


def collect_slack_messages(channel_id, oldest, latest):
    url = f"https://slack.com/api/conversations.history?channel={channel_id}&oldest={oldest}&latest={latest}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    )
    with urllib.request.urlopen(req) as res:
        result = json.loads(res.read().decode("utf-8"))

    messages = result.get("messages", [])
    filtered = [
        msg for msg in messages
        if msg.get("subtype") is None and msg.get("bot_id") is None
    ]
    return filtered


def get_slack_user_name(user_id):
    url = f"https://slack.com/api/users.info?user={user_id}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    )
    try:
        with urllib.request.urlopen(req) as res:
            result = json.loads(res.read().decode("utf-8"))
        if not result.get("ok"):
            print(f"users.info 조회 실패 ({user_id}): {result.get('error')}")
            return None

        user = result.get("user", {})
        profile = user.get("profile", {})
        return profile.get("display_name") or profile.get("real_name") or user.get("real_name")
    except Exception as e:
        print(f"users.info 호출 실패 ({user_id}): {e}")
        return None


def resolve_assignee_name(assignee):
    if not assignee:
        return assignee

    mention_match = re.search(r"<@([UW][A-Z0-9]+)>", assignee)
    if mention_match:
        user_id = mention_match.group(1)
    elif re.fullmatch(r"[UW][A-Z0-9]{6,}", assignee.strip()):
        user_id = assignee.strip()
    else:
        return assignee

    print(f"get_slack_user_name 호출 시작: user_id={user_id}")
    name = get_slack_user_name(user_id)
    print(f"get_slack_user_name 호출 완료: user_id={user_id}, name={name}")
    return name if name else assignee


def collect_cloudwatch_logs(oldest_ts, latest_ts):
    client = boto3.client("logs", region_name="ap-northeast-2")
    log_groups = [
        "/aws/lambda/yp-lambda-fastapi",
        "/aws/lambda/yp-lambda-alarm",
        "/aws/lambda/yp-lambda-postmortem"
    ]

    all_logs = []
    start_ms = int(oldest_ts * 1000)
    end_ms = int(latest_ts * 1000)

    for log_group in log_groups:
        try:
            response = client.filter_log_events(
                logGroupName=log_group,
                startTime=start_ms,
                endTime=end_ms,
                filterPattern="?ERROR ?error ?Exception ?exception"
            )
            for event in response.get("events", []):
                all_logs.append(f"[{log_group}] {event['message'].strip()}")
        except Exception as e:
            print(f"CloudWatch 로그 수집 실패 {log_group}: {e}")

    return "\n".join(all_logs) if all_logs else "수집된 에러 로그 없음"


def collect_cloudwatch_metrics(oldest_ts, latest_ts):
    client = boto3.client("cloudwatch", region_name="ap-northeast-2")
    start_time = datetime.utcfromtimestamp(oldest_ts)
    end_time = datetime.utcfromtimestamp(latest_ts)
    ec2_instance_id = os.environ.get("EC2_INSTANCE_ID", "")

    metrics = []

    try:
        response = client.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[{"Name": "InstanceId", "Value": ec2_instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average", "Maximum"]
        )
        for point in response.get("Datapoints", []):
            metrics.append(f"[CPU] {point['Timestamp']} - 평균: {point['Average']:.1f}%, 최대: {point['Maximum']:.1f}%")
    except Exception as e:
        print(f"CPU 메트릭 수집 실패: {e}")

    try:
        response = client.get_metric_statistics(
            Namespace="CWAgent",
            MetricName="mem_used_percent",
            Dimensions=[{"Name": "InstanceId", "Value": ec2_instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average", "Maximum"]
        )
        for point in response.get("Datapoints", []):
            metrics.append(f"[Memory] {point['Timestamp']} - 평균: {point['Average']:.1f}%, 최대: {point['Maximum']:.1f}%")
    except Exception as e:
        print(f"메모리 메트릭 수집 실패: {e}")

    return "\n".join(metrics) if metrics else "수집된 메트릭 없음"


def call_claude_api(messages, cloudwatch_logs=""):
    slack_text = "\n".join([
        f"[{msg.get('user', 'unknown')}] {msg.get('text', '')}"
        for msg in messages
    ])

    prompt = f"""당신은 10년 이상의 경력을 가진 IT 장애 분석 전문가(SRE)입니다. 아래 슬랙 대화와 CloudWatch 로그/메트릭을 근거로, 실제 운영팀이 그대로 활용할 수 있는 수준의 상세하고 구체적인 Postmortem 문서를 JSON 형식으로 작성해주세요.

[슬랙 대화]
{slack_text}

[CloudWatch 로그 및 메트릭]
{cloudwatch_logs}

작성 원칙:
- 모든 서술형 항목(summary, root_cause, resolution, prevention, affected_range, similar_incidents)은 각각 최소 3~5문장 이상으로, 근거(슬랙 발언, 로그 메시지, 메트릭 수치 등)를 인용하며 구체적으로 작성하세요.
- 슬랙 대화나 로그에서 직접 확인되지 않는 내용은 추측임을 명시하고("~로 추정됨", "~일 가능성이 있음"), 근거 없이 단정하지 마세요.
- 각 문장은 "무엇이, 왜, 어떤 영향으로" 이어지는 인과관계를 담아 서술하세요. 두루뭉술한 표현("문제가 발생했다", "조치를 취했다") 대신 구체적인 대상(서비스명, 컴포넌트, 에러 메시지, 수치)을 명시하세요.

각 필드별 세부 지침:
- timeline: 장애 발생부터 종료까지의 과정을 시간순으로 정리하되, 각 이벤트마다 "HH:MM - 이벤트 내용" 형식의 줄로 구성하고 최소 5개 이상의 이벤트를 포함하세요. 슬랙 메시지 타임스탬프, 로그 발생 시각, 메트릭 이상 시점을 근거로 실제 시각을 사용하고, 각 줄에는 무슨 일이 있었고 누가 어떤 조치를 했는지(감지, 보고, 원인 파악, 조치 시도, 해결, 확인)를 구체적으로 기술하세요.
- root_cause: 근본 원인을 기술적으로 분석하세요. (1) 직접적 트리거(어떤 이벤트/배포/트래픽 변화가 문제를 유발했는지), (2) 장애가 전파된 기술적 메커니즘(어떤 컴포넌트가 어떻게 실패했는지, 관련 로그의 에러 메시지나 메트릭 수치 인용), (3) 왜 기존 시스템/모니터링/코드가 이를 막지 못했는지(설계상 취약점, 임계값 미비, 예외 처리 누락 등)를 각각 문단으로 나누어 설명하세요.
- resolution: 실제로 취해진 조치를 시간순/단계별로 구체적으로 서술하세요. 어떤 명령/조작/설정 변경을 했는지, 왜 그 방법을 선택했는지, 적용 후 어떻게 정상화를 확인했는지(어떤 메트릭/로그/사용자 반응으로 확인했는지)를 포함하세요.
- prevention: 재발 방지 대책을 실행 가능한 액션 아이템 목록으로 작성하세요. 최소 4개 이상의 항목을 "- [담당 영역] 구체적 액션 (예상 효과)" 형식으로 나열하고, 단기(즉시 적용 가능한 핫픽스/알람 추가)와 중장기(아키텍처 개선, 자동화, 프로세스 변경)로 구분하세요. "모니터링 강화", "코드 리뷰 철저히" 같은 추상적 표현 대신 구체적인 지표명, 임계값, 도구명을 명시하세요.
- affected_range: 영향을 받은 서비스/기능, 예상 사용자 수 또는 요청 수, 영향의 성격(전체 장애/부분 성능 저하/특정 지역·기능 한정 등)을 구체적으로 기술하세요.
- similar_incidents: 슬랙 대화와 로그에서 나타난 키워드, 에러 유형, 리소스(CPU/메모리/DB 커넥션 등) 패턴을 근거로 유사 장애 카테고리를 추론하고, 왜 그렇게 판단했는지 근거를 함께 제시하세요.

다음 JSON 형식으로 응답해주세요. JSON 외에 다른 텍스트는 포함하지 마세요:
{{
  "started_at": "장애 발생 시각",
  "ended_at": "장애 종료 시각",
  "downtime": "총 다운타임 (예: 1시간 30분)",
  "summary": "장애 요약 (핵심 사건, 원인, 영향, 해결 결과를 포함한 3~5문장)",
  "severity": "Critical/Warning/Info 중 하나",
  "timeline": "HH:MM - 이벤트 형식의 줄바꿈된 타임라인 (최소 5개 이벤트, 시간순)",
  "root_cause": "트리거/전파 메커니즘/재발 가능 이유를 포함한 기술적 근본 원인 분석 (최소 3~5문장)",
  "resolution": "단계별 해결 과정과 정상화 확인 방법 (최소 3~5문장)",
  "prevention": "단기/중장기로 구분된 구체적 액션 아이템 목록 (최소 4개 항목)",
  "affected_range": "영향 범위 (서비스, 기능, 사용자/요청 수, 영향 성격) (최소 3문장)",
  "assignee": "주요 담당자 (슬랙 대화에서 파악)",
  "similar_incidents": "유사 장애 패턴과 그 판단 근거 (카테고리, 키워드, 원인 기반, 최소 3문장)"
}}"""

    data = json.dumps({
        "model": "claude-sonnet-4-5",
        "max_tokens": 8000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=data,
        headers={
            "Content-Type": "application/json",
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01"
        }
    )
    with urllib.request.urlopen(req) as res:
        result = json.loads(res.read().decode("utf-8"))
        response_text = result["content"][0]["text"]

        try:
            clean_text = response_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            return json.loads(clean_text.strip())
        except json.JSONDecodeError:
            return {"summary": response_text, "error": "JSON 파싱 실패"}


def save_to_rds(postmortem_data, messages, incident_id=None):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # postmortems 테이블 저장
            cursor.execute("""
                INSERT INTO postmortems 
                (incident_id, summary, timeline, root_cause, resolution, prevention, 
                affected_range, assignee, similar_incidents, is_ai_generated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                incident_id,
                postmortem_data.get("summary", ""),
                postmortem_data.get("timeline", ""),
                postmortem_data.get("root_cause", ""),
                postmortem_data.get("resolution", ""),
                postmortem_data.get("prevention", ""),
                postmortem_data.get("affected_range", ""),
                postmortem_data.get("assignee", ""),
                postmortem_data.get("similar_incidents", ""),
                True
            ))

            # slack_messages 테이블 저장
            if incident_id:
                for msg in messages:
                    cursor.execute("""
                        INSERT INTO slack_messages (incident_id, user_name, message, timestamp)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        incident_id,
                        msg.get("user", "unknown"),
                        msg.get("text", ""),
                        msg.get("ts", "")
                    ))

        conn.commit()
        print("RDS 저장 완료")
        return True
    except Exception as e:
        print(f"RDS 저장 실패: {e}")
        return False
    finally:
        conn.close()


def handler(event, context):
    print(f"받은 이벤트: {json.dumps(event)}")

    body = {}
    if isinstance(event.get("body"), str):
        from urllib.parse import parse_qs
        parsed = parse_qs(event["body"])
        body = {k: v[0] for k, v in parsed.items()}

    command = body.get("command", "")
    channel_id = body.get("channel_id", SLACK_CHANNEL_ID)
    user_name = body.get("user_name", "unknown")

    if command != "/resolve":
        return {
            "statusCode": 200,
            "body": json.dumps({"text": "알 수 없는 명령어입니다."})
        }

    ended_at = datetime.utcnow()
    ended_at_str = ended_at.strftime("%Y-%m-%d %H:%M:%S UTC")

    # RDS에서 활성 장애 조회
    active_incident = get_active_incident()
    incident_id = None
    downtime = None
    oldest_ts = ended_at.timestamp() - 86400

    if active_incident:
        incident_id = active_incident["id"]
        started_at = active_incident["started_at"]
        downtime_seconds = (ended_at - started_at).total_seconds()
        downtime = downtime_seconds / 60  # 분 단위
        oldest_ts = started_at.timestamp()
        update_incident_resolved(incident_id, ended_at, downtime)
        print(f"장애 종료 처리: incident_id={incident_id}, downtime={downtime:.1f}분")
    else:
        print("활성 장애 없음, 기본값으로 처리")

    latest_ts = ended_at.timestamp()
    messages = collect_slack_messages(channel_id, oldest_ts, latest_ts)
    message_count = len(messages)

    cloudwatch_logs = collect_cloudwatch_logs(oldest_ts, latest_ts)
    cloudwatch_metrics = collect_cloudwatch_metrics(oldest_ts, latest_ts)
    cloudwatch_data = f"{cloudwatch_logs}\n\n[메트릭]\n{cloudwatch_metrics}"

    postmortem_draft = call_claude_api(messages, cloudwatch_data)
    postmortem_draft["is_ai_generated"] = True
    postmortem_draft["assignee"] = resolve_assignee_name(postmortem_draft.get("assignee", ""))

    save_to_rds(postmortem_draft, messages, incident_id)

    downtime_str = f"{downtime:.1f}분" if downtime else "계산 불가"
    dashboard_url = os.environ.get("DASHBOARD_URL", "https://your-cloudfront-url.com")
    postmortem_link = (
        f"{dashboard_url}/incidents/{incident_id}/postmortem"
        if incident_id else dashboard_url
    )
    send_slack_message(
        channel_id,
        f"✅ *장애 종료 처리 완료*\n"
        f"*종료 시각:* {ended_at_str}\n"
        f"*처리자:* {user_name}\n"
        f"*다운타임:* {downtime_str}\n"
        f"*수집된 대화:* {message_count}건\n"
        f"*Postmortem 문서:* {postmortem_link}\n"
        f"Postmortem 문서 자동 생성을 시작합니다..."
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"text": f"장애 종료 처리 완료. 종료 시각: {ended_at_str}"})
    }