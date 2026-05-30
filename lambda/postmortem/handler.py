import json
import os
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

    prompt = f"""당신은 IT 장애 분석 전문가입니다. 아래 슬랙 대화와 CloudWatch 로그를 분석하여 Postmortem 문서를 JSON 형식으로 작성해주세요.

[슬랙 대화]
{slack_text}

[CloudWatch 로그 및 메트릭]
{cloudwatch_logs}

다음 JSON 형식으로 응답해주세요. JSON 외에 다른 텍스트는 포함하지 마세요:
{{
  "started_at": "장애 발생 시각",
  "ended_at": "장애 종료 시각",
  "downtime": "총 다운타임 (예: 1시간 30분)",
  "summary": "장애 요약 (2-3문장)",
  "severity": "Critical/Warning/Info 중 하나",
  "timeline": "장애 타임라인 (시간순 정리)",
  "root_cause": "근본 원인 분석",
  "resolution": "해결 방법",
  "prevention": "재발 방지 대책",
  "affected_range": "영향 범위 (서비스, 사용자 수 등)",
  "assignee": "주요 담당자 (슬랙 대화에서 파악)",
  "similar_incidents": "슬랙 대화와 로그에서 파악된 유사 장애 패턴 (카테고리, 키워드, 원인 기반으로 추론)"
}}"""

    data = json.dumps({
        "model": "claude-sonnet-4-5",
        "max_tokens": 4000,
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

    save_to_rds(postmortem_draft, messages, incident_id)

    downtime_str = f"{downtime:.1f}분" if downtime else "계산 불가"
    dashboard_url = os.environ.get("DASHBOARD_URL", "https://your-cloudfront-url.com")
    send_slack_message(
        channel_id,
        f"✅ *장애 종료 처리 완료*\n"
        f"*종료 시각:* {ended_at_str}\n"
        f"*처리자:* {user_name}\n"
        f"*다운타임:* {downtime_str}\n"
        f"*수집된 대화:* {message_count}건\n"
        f"*Postmortem 문서:* {dashboard_url}/postmortem\n"
        f"Postmortem 문서 자동 생성을 시작합니다..."
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"text": f"장애 종료 처리 완료. 종료 시각: {ended_at_str}"})
    }