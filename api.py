from fastapi import FastAPI

from api_router import router as api_router
from auto_router import router as auto_router
from env_loader import *
from logging_config import *

app = FastAPI(
    title="MCP REST API",
    version="1.0.0"
)

app.include_router(auto_router)
app.include_router(api_router)