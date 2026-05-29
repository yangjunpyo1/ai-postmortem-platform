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

    # 봇 메시지 필터링 (사람 대화만)
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


def call_claude_api(messages, cloudwatch_logs=""):
    # TODO: M3에서 프롬프트 설계 완성
    prompt = f"""
슬랙 대화와 CloudWatch 로그를 분석하여 Postmortem 문서를 작성해주세요.

[슬랙 대화]
{json.dumps(messages, ensure_ascii=False, indent=2)}

[CloudWatch 로그]
{cloudwatch_logs}
"""
    data = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
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
        return result["content"][0]["text"]


def handler(event, context):
    # 슬랙 슬래시 명령어 파싱
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

    # 종료 시각 기록
    ended_at = datetime.utcnow()
    ended_at_str = ended_at.strftime("%Y-%m-%d %H:%M:%S UTC")

    # 슬랙 대화 수집 (최근 24시간)
    latest_ts = ended_at.timestamp()
    oldest_ts = latest_ts - 86400  # 24시간

    messages = collect_slack_messages(channel_id, oldest_ts, latest_ts)
    message_count = len(messages)

    # CloudWatch 로그 수집
    cloudwatch_logs = collect_cloudwatch_logs(oldest_ts, latest_ts)

    # Claude API 호출
    postmortem_draft = call_claude_api(messages, cloudwatch_logs)

    # 완료 알림 전송
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