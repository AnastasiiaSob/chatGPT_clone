from fastapi import FastAPI

from src.routes.v1.endpoints import router as v1_router

app = FastAPI(title="ChatGPT Clone API")

app.include_router(v1_router, prefix="/api/v1", tags=["v1"])

