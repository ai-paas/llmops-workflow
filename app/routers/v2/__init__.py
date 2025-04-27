from fastapi import APIRouter

from .endpoints.health import router as health_router
from .endpoints.models import router as models_router
from .endpoints.datasets import router as datasets_router
from .endpoints.prompts import router as prompts_router
from .endpoints.serving import router as serving_router
from .endpoints.workflows import router as workflows_router

api_router = APIRouter(prefix="/api/v2")

api_router.include_router(health_router)
api_router.include_router(models_router)
api_router.include_router(datasets_router)
api_router.include_router(prompts_router)
api_router.include_router(serving_router)
api_router.include_router(workflows_router)