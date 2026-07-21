from fastapi import FastAPI

from app.config import settings
from app.db import Base, engine
from app.routers import use_cases

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Reference library of AI use cases, matched to readiness/maturity results.",
    version="0.1.0",
)

app.include_router(use_cases.router)


@app.get("/health")
def health():
    return {"status": "ok"}
