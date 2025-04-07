from fastapi import APIRouter

from .endpoints.health import router as health_router

api_router = APIRouter(prefix="/api/v2")

api_router.include_router(health_router)
