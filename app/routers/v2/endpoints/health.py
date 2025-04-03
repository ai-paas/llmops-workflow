# core/health.py
from fastapi import APIRouter, HTTPException
from core.exceptions import ItemNotFoundException
from pydantic import BaseModel

router = APIRouter()


class HealthRequest(BaseModel):
    status: str

class HealthResponse(BaseModel):
    status: str
    version: str

@router.post("/health", response_model=HealthResponse)
async def health(request: HealthRequest):
    return HealthResponse(status="ok", version="1.0.0")


@router.get("/success")
async def success():
    data = {"message": "This is a successful response"}
    return data

@router.get("/custom-exception")
async def custom_exception():
    raise ItemNotFoundException

@router.get("/http-exception")
async def http_exception():
    raise HTTPException(status_code=404, detail="Item not found")

@router.get("/unhandled-exception")
async def unhandled_exception():
    raise ValueError("This is an unhandled exception")
