import json
import os
import urllib.request

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")


def get_severity_from_alarm_name(alarm_name):
    alarm_name_lower = alarm_name.lower()
    if "critical" in alarm_name_lower:
        return "critical"
    elif "warning" in alarm_name_lower:
        return "warning"
    else:
        return "info"


def build_message(severity, alarm_name, description):
    if severity == "critical":
        return {
            "channel": SLACK_CHANNEL_ID,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"🔴 *[CRITICAL] 장애 발생*\n*알람:* {alarm_name}\n*내용:* {description}\n<!channel>"
                    }
                }
            ]
        }
    elif severity == "warning":
        return {
            "channel": SLACK_CHANNEL_ID,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"🟡 *[WARNING] 경고 발생*\n*알람:* {alarm_name}\n*내용:* {description}"
                    }
                }
            ]
        }
    else:
        return {
            "channel": SLACK_CHANNEL_ID,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"🟢 *[INFO] 정보 알림*\n*알람:* {alarm_name}\n*내용:* {description}"
                    }
                }
            ]
        }


def send_slack_message(message):
    data = json.dumps(message).encode("utf-8")
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


def handler(event, context):
    for record in event.get("Records", []):
        body = json.loads(record["body"])
        message = json.loads(body.get("Message", "{}"))

        alarm_name = message.get("AlarmName", "Unknown")
        description = message.get("AlarmDescription", "설명 없음")

        severity = get_severity_from_alarm_name(alarm_name)
        slack_message = build_message(severity, alarm_name, description)
        result = send_slack_message(slack_message)

        print(f"Severity: {severity}, Alarm: {alarm_name}, Slack result: {result}")

    return {"statusCode": 200}