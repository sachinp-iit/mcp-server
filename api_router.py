from fastapi import APIRouter
from tools import registry
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/registry/create")
def create_record(key: str, value: str):
    return registry.create_record(key, value)


@router.get("/registry/get")
def get_record(key: str):
    return registry.get_record(key)


@router.put("/registry/update")
def update_record(key: str, value: str):
    return registry.update_record(key, value)


@router.delete("/registry/delete")
def delete_record(key: str):
    return registry.delete_record(key)


@router.get("/registry/list")
def list_records():
    return registry.list_records()

