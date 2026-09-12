import inspect

from fastapi import APIRouter, Depends
from pydantic import create_model

from auth import require_api_key
from logging_config import audit_logger
from tools import files, nlp, postgres, registry

router = APIRouter(
    dependencies=[Depends(require_api_key)]
)

# Map REST paths to Python callables
TOOLS = {
    "postgres/execute": postgres.execute_sql,
    "postgres/schema": postgres.get_schema,
    "nlp/classify": nlp.classify_intent,
    "nlp/generate_sql": nlp.generate_sql,
    "registry/resolve": registry.resolve_tool_by_intent,
    "files/list": files.list_files
}

for path, func in TOOLS.items():
    sig = inspect.signature(func)

    fields = {
    	name: (param.annotation, ...)
    	for name, param in inspect.signature(func).parameters.items()
    }

    # Dynamically building the request model
    RequestModel = create_model(
        f"{func.__name__}Request",
        **fields
    )

    async def endpoint(payload: RequestModel, f=func):
        audit_logger.info(
            "REST_CALL | %s | %s",
            f.__name__,
            payload.dict()
        )
        result = f(**payload.dict())
        audit_logger.info(
            "REST_RESULT | %s | %s",
            f.__name__,
            result
        )
        return result

    router.post(f"/{path}")(endpoint)