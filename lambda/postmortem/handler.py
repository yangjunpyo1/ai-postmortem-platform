import json
import os
import urllib.request
import boto3
from datetime import datetime

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")


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
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 2000,
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
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {"summary": response_text, "error": "JSON 파싱 실패"}


def save_to_rds(postmortem_data, messages):
    # TODO: M4에서 RDS 연동 후 구현
    # incidents 테이블 저장
    # postmortems 테이블 저장
    # slack_messages 테이블 저장
    print(f"RDS 저장 예정 데이터: {json.dumps(postmortem_data, ensure_ascii=False)}")
    return True


def handler(event, context):
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

    latest_ts = ended_at.timestamp()
    oldest_ts = latest_ts - 86400

    messages = collect_slack_messages(channel_id, oldest_ts, latest_ts)
    message_count = len(messages)

    cloudwatch_logs = collect_cloudwatch_logs(oldest_ts, latest_ts)
    cloudwatch_metrics = collect_cloudwatch_metrics(oldest_ts, latest_ts)
    cloudwatch_data = f"{cloudwatch_logs}\n\n[메트릭]\n{cloudwatch_metrics}"

    postmortem_draft = call_claude_api(messages, cloudwatch_data)
    postmortem_draft["is_ai_generated"] = True

    # RDS 저장 (M4에서 구현 완성)
    save_to_rds(postmortem_draft, messages)

    dashboard_url = os.environ.get("DASHBOARD_URL", "https://your-cloudfront-url.com")
    send_slack_message(
        channel_id,
        f"✅ *장애 종료 처리 완료*\n"
        f"*종료 시각:* {ended_at_str}\n"
        f"*처리자:* {user_name}\n"
        f"*수집된 대화:* {message_count}건\n"
        f"*Postmortem 문서:* {dashboard_url}/postmortem\n"
        f"Postmortem 문서 자동 생성을 시작합니다..."
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"text": f"장애 종료 처리 완료. 종료 시각: {ended_at_str}"})
    }