from fastapi import FastAPI
from mangum import Mangum
from app.api import auth, incidents, postmortems, statistics, similar

app = FastAPI(
    title="AI Postmortem Platform",
    description="AI 기반 장애 Postmortem 자동화 플랫폼",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(incidents.router)
app.include_router(postmortems.router)
app.include_router(statistics.router)
app.include_router(similar.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Lambda 핸들러
handler = Mangum(app)