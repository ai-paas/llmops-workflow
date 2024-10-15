from fastapi import APIRouter

from .evaluation import evaluation_router as evluation_router
from .knowledge import knowledge_router
from .model import model_router
from .prompt import prompt_router
from .solution import solution_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(model_router)
api_router.include_router(knowledge_router)
api_router.include_router(evluation_router)
api_router.include_router(prompt_router)
api_router.include_router(solution_router)
