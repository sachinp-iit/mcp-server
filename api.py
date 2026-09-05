from env_loader import *
from logging_config import *
from fastapi import FastAPI
from auto_router import router as auto_router
from api_router import router as api_router

app = FastAPI(
    title="MCP REST API",
    version="1.0.0"
)

app.include_router(auto_router)
app.include_router(api_router)