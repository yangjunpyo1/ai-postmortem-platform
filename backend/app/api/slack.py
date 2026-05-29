from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import boto3
import json

router = APIRouter(prefix="/slack", tags=["slack"])


@router.post("/events")
async def slack_events(request: Request):
    body = await request.json()

    if body.get("type") == "url_verification":
        return JSONResponse(content={"challenge": body.get("challenge")})

    return JSONResponse(content={"status": "ok"})


@router.post("/commands")
async def slack_commands(request: Request):
    body = await request.form()
    command = body.get("command", "")
    channel_id = body.get("channel_id", "")
    user_name = body.get("user_name", "")

    if command == "/resolve":
        # yp-lambda-postmortem 비동기 트리거
        try:
            lambda_client = boto3.client("lambda", region_name="ap-northeast-2")
            lambda_client.invoke(
                FunctionName="yp-lambda-postmortem",
                InvocationType="Event",
                Payload=json.dumps({
                    "body": f"command=/resolve&channel_id={channel_id}&user_name={user_name}"
                })
            )
        except Exception as e:
            print(f"Lambda 트리거 실패: {e}")

        return JSONResponse(content={
            "response_type": "in_channel",
            "text": "장애 종료 처리 중입니다... Postmortem 문서를 자동 생성합니다."
        })

    return JSONResponse(content={"text": "알 수 없는 명령어입니다."})