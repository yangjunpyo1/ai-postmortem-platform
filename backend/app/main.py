from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum
from app.api import auth, incidents, postmortems, statistics, similar, slack
from app.database import Base, engine
from app.models import user, incident, postmortem, slack_message

app = FastAPI(
    title="AI Postmortem Platform",
    version="1.0.0",
    root_path="/dev"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str):
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,PATCH,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(incidents.router)
app.include_router(postmortems.router)
app.include_router(statistics.router)
app.include_router(similar.router)
app.include_router(slack.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

handler = Mangum(app, lifespan="off", api_gateway_base_path="/dev")
#
