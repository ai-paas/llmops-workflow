from datetime import datetime
from typing import Annotated
from urllib.parse import quote

from config.db.connect import SessionDepends
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from schemas.prompt import (
    PromptCreateSchema,
    PromptReadSchema,
    PromptVariableBaseSchema,
    PromptVariableReadSchema,
)
from services.prompt_service import PromptService, PromptVariableService
from sqlalchemy.orm import Session

prompt_router = APIRouter(prefix="/prompts", tags=["Prompts"])


@prompt_router.post("", response_model=PromptReadSchema)
def create_prompt(prompt_base: PromptCreateSchema, db: Session = SessionDepends):
    """
    새로운 프롬프트를 생성합니다.

    Args:
        prompt_base (PromptCreateSchema): 생성할 프롬프트의 스키마.
        db (Session): 데이터베이스 세션.

    Returns:
        생성된 프롬프트 객체.

    Raises:
        Exception: 프롬프트 생성 중 에러 발생 시.
    """
    try:
        result = PromptService().create(db, prompt_base)
        db.commit()
        return result
    except Exception:
        raise ("Error has been Occured!")


@prompt_router.put("/{prompt_id}", response_model=PromptReadSchema)
def update_prompt(prompt_id: int, prompt_base: PromptCreateSchema, db: Session = SessionDepends):
    """
    기존의 프롬프트를 업데이트합니다.

    Args:
        prompt_id (int): 업데이트할 프롬프트의 ID.
        prompt_base (PromptCreateSchema): 업데이트할 프롬프트의 스키마.
        db (Session): 데이터베이스 세션.

    Returns:
        업데이트된 프롬프트 객체.

    Raises:
        Exception: 프롬프트 업데이트 중 에러 발생 시.
    """
    try:
        db_obj = PromptService().get(db, prompt_id)
        result = PromptService().update(db, db_obj, prompt_base)
        db.commit()
        return result
    except Exception:
        raise ("Error has been Occured!")


@prompt_router.get("/{prompt_id}", response_model=PromptReadSchema)
def read_prompt(prompt_id: int, db: Session = SessionDepends):
    """
    특정 프롬프트를 조회합니다.

    Args:
        prompt_id (int): 조회할 프롬프트의 ID.
        db (Session): 데이터베이스 세션.

    Returns:
        조회된 프롬프트 객체.

    Raises:
        Exception: 프롬프트 조회 중 에러 발생 시.
    """
    try:
        result = PromptService().get(db, prompt_id)
        return result
    except Exception:
        raise ("Error has been Occured!")


@prompt_router.get("", response_model=list[PromptReadSchema])
def read_prompts(skip: int = 0, limit: int = 10, db: Session = SessionDepends):
    """
    여러 프롬프트를 조회합니다.

    Args:
        skip (int): 조회를 시작할 인덱스 (기본값: 0).
        limit (int): 조회할 프롬프트 수 (기본값: 10).
        db (Session): 데이터베이스 세션.

    Returns:
        조회된 프롬프트 리스트.

    Raises:
        Exception: 프롬프트 조회 중 에러 발생 시.
    """
    try:
        result = PromptService().get_multi(db, skip, limit)
        return result
    except Exception:
        raise ("Error has been Occured!")
