import itertools
from datetime import datetime
from typing import Annotated, Any
from urllib.parse import quote

from config.db.connect import SessionDepends
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from schemas.evaluation import RetrievalRequestSchema
from schemas.solution import (
    SolutionBaseSchema,
    SolutionConfigBaseSchema,
    SolutionConfigCreateSchema,
    SolutionCreateSchema,
    SolutionReadSchema,
)
from services.evaluation_service import EvaluationService
from services.knowledge_service import KnowledgeService
from services.solution_service import (
    SolutionConfigService,
    SolutionService,
)
from services.prompt_service import (
    PromptService
)
from sqlalchemy.orm import Session
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from config.settings import get_settings

solution_router = APIRouter(prefix="/solutions", tags=["Solutions"])
settings = get_settings()

@solution_router.post("/{solution_id}/generates/text")
def generate_text(
    solution_id: int,
    prompt_id: int=1,
    messages: list[dict[str, str]]=[
        {"role": "assistant", "content": "You are ahelpful assistant"},
        {"role": "user", "content": "Where is the capital of Korea?"}
    ], 
    db: Session = SessionDepends
):
    # DB에서 필요정보 불러오기
    solution_obj = SolutionService().get(db, solution_id)
    solution_config = solution_obj.solution_config
    solution_knowledge = solution_obj.knowledge
    prompt = PromptService().get(db, prompt_id).content

    question = messages[-1].get("content")

    # Retrieve
    contexts = EvaluationService.retrieve(
        RetrievalRequestSchema(
            query=question,
            knowledge_id=solution_knowledge.id,
            search_type_id=solution_knowledge.search_type.id,
            top_k=solution_knowledge.top_k,
            threshold_score=solution_knowledge.score,
            dense_weight=0.6,
            sparse_weight=0.4,
        ),
        db,
    )
    context: list[str] = "\n".join(item.get("text") for item in contexts)

    # Prompt rntjd
    content = prompt.format(context=context, question=question)
    messages[-1]["content"] = content

    # Model Load
    # TODO: user_id를 받아오도록 수정
    user_id = "default"
    user_pipeline = settings.USER_MODELS.get(user_id, {})
    if not user_pipeline:
        raise HTTPException("Model을 먼저 Load 하세요.")
    model = user_pipeline.get("model")
    tokenizer = user_pipeline.get("tokenizer")
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    # TODO: max_length 수정
    result = pipe(prompt, max_length=1024)
    return result[0]["generated_text"]


@solution_router.post("", response_model=SolutionReadSchema)
def create_solution(request: SolutionCreateSchema, db: Session = SessionDepends):
    """
    새로운 솔루션과 그 구성을 생성합니다.

    Args:
        request (SolutionCreateSchema): 생성할 솔루션 데이터와 구성.
        db (Session): 데이터베이스 세션 종속성.

    Returns:
        SolutionReadSchema: 생성된 솔루션의 상세 정보.
    """
    solution_obj = SolutionService().create(db, request.solution)
    solution_id = solution_obj.id
    solution_config = SolutionConfigBaseSchema(solution_id=solution_id, **request.solution_config.model_dump())
    SolutionConfigService().create(db, solution_config)
    result = SolutionService().get(db, solution_id)
    db.commit()
    return result


@solution_router.put("/{solution_id}", response_model=SolutionReadSchema)
def update_solution(solution_id: int, request: SolutionBaseSchema, db: Session = SessionDepends):
    """
    기존 솔루션을 업데이트합니다.

    Args:
        solution_id (int): 업데이트할 솔루션의 ID.
        request (SolutionBaseSchema): 업데이트된 솔루션 데이터.
        db (Session): 데이터베이스 세션 종속성.

    Returns:
        SolutionReadSchema: 업데이트된 솔루션의 상세 정보.
    """
    db_obj = SolutionService().get(db, solution_id)
    result = SolutionService().update(db, db_obj, request)
    db.commit()
    return result


@solution_router.put("/{solution_id}/configs/{solution_config_id}", response_model=SolutionReadSchema)
def update_solution_config(
    solution_id: int, solution_config_id: int, request: SolutionConfigCreateSchema, db: Session = SessionDepends
):
    """
    기존 솔루션의 구성을 업데이트합니다.

    Args:
        solution_id (int): 솔루션의 ID.
        solution_config_id (int): 업데이트할 솔루션 구성의 ID.
        request (SolutionConfigCreateSchema): 업데이트된 구성 데이터.
        db (Session): 데이터베이스 세션 종속성.

    Returns:
        SolutionReadSchema: 새로운 구성으로 업데이트된 솔루션의 상세 정보.
    """
    db_obj = SolutionConfigService().get(db, solution_config_id)
    solution_config = SolutionConfigBaseSchema(solution_id=solution_id, **request.model_dump())
    SolutionConfigService().update(db, db_obj, solution_config)
    result = SolutionService().get(db, solution_id)
    db.commit()
    return result


@solution_router.get("/{solution_id}", response_model=SolutionReadSchema)
def read_solution(solution_id: int, db: Session = SessionDepends):
    """
    솔루션 ID로 솔루션을 조회합니다.

    Args:
        solution_id (int): 조회할 솔루션의 ID.
        db (Session): 데이터베이스 세션 종속성.

    Returns:
        SolutionReadSchema: 조회된 솔루션의 상세 정보.
    """
    result = SolutionService().get(db, solution_id)
    return result


@solution_router.get("", response_model=list[SolutionReadSchema])
def read_solutions(skip: int = 0, limit: int = 10, db: Session = SessionDepends):
    """
    솔루션 목록을 페이지네이션 옵션과 함께 조회합니다.

    Args:
        skip (int, optional): 페이지네이션을 위한 건너뛸 레코드 수. 기본값은 0.
        limit (int, optional): 반환할 최대 레코드 수. 기본값은 10.
        db (Session): 데이터베이스 세션 종속성.

    Returns:
        list[SolutionReadSchema]: 솔루션 목록.
    """
    result = SolutionService().get_multi(db, skip, limit)
    return result
