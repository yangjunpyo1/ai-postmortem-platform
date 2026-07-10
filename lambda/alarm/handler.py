import json
import os
import urllib.request
from datetime import datetime
import pymysql

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
DB_HOST = os.environ.get("DB_HOST", "").split(":")[0]
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
AUTO_INCIDENT_USER_ID = int(os.environ.get("AUTO_INCIDENT_USER_ID", "1"))

SEVERITY_DB_MAP = {
    "critical": "Critical",
    "warning": "Warning",
    "info": "Info",
}


def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )


def get_severity_from_alarm_name(alarm_name):
    alarm_name_lower = alarm_name.lower()
    if "critical" in alarm_name_lower:
        return "critical"
    elif "warning" in alarm_name_lower:
        return "warning"
    else:
        return "info"


def get_category_from_alarm_name(alarm_name):
    alarm_name_lower = alarm_name.lower()
    if "cpu" in alarm_name_lower or "memory" in alarm_name_lower:
        return "서버"
    elif "rds" in alarm_name_lower:
        return "DB"
    elif "lambda" in alarm_name_lower:
        return "애플리케이션"
    elif "apigw" in alarm_name_lower or "natgw" in alarm_name_lower:
        return "네트워크"
    else:
        return "기타"


def create_incident(title, severity, category, started_at):
    try:
        conn = get_db_connection()
        now = datetime.utcnow()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO incidents (user_id, title, severity, category, status, started_at, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (AUTO_INCIDENT_USER_ID, title, severity, category, "발생중", started_at, now, now)
            )
            incident_id = cursor.lastrowid
        conn.commit()
        print(f"장애 자동 등록 완료: incident_id={incident_id}, severity={severity}, category={category}")
        return incident_id
    except Exception as e:
        print(f"장애 자동 등록 실패: {e}")
        return None
    finally:
        conn.close()


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
        category = get_category_from_alarm_name(alarm_name)

        slack_message = build_message(severity, alarm_name, description)
        result = send_slack_message(slack_message)

        create_incident(
            title=description,
            severity=SEVERITY_DB_MAP[severity],
            category=category,
            started_at=datetime.utcnow()
        )

        print(f"Severity: {severity}, Category: {category}, Alarm: {alarm_name}, Slack result: {result}")

    return {"statusCode": 200}
