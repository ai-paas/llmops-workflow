from datetime import datetime
from typing import Annotated, Optional, Any

from config.db.connect import SessionDepends
from fastapi import APIRouter, Form, HTTPException, UploadFile
from fastapi.security import APIKeyHeader
from schemas.model import ModelBaseSchema, ModelReadSchema
from services.model_service import (
    CustomModelService,
    HuggingFaceModelService,
    ModelService,
)
from sqlalchemy.orm import Session
from config.settings import get_settings

model_router = APIRouter(prefix="/models", tags=["Models"])

settings = get_settings()
# API_KEY_HEADER = APIKeyHeader(name="X-API-Key")


# TODO: 책임 분리 필요.
@model_router.post("", response_model=ModelReadSchema)
def create_model(
    *,
    db: Session = SessionDepends,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    model_provider_id: Annotated[int, Form()],
    model_type_id: Annotated[int, Form()],
    model_format_id: Annotated[int, Form()],
    file: UploadFile | None = None,
):
    """
    Model Registry에 Model을 등록하는 API

    * params
        - model_provider
            1. huggingface
            2. ollama
            3. custom
        - model_type
            1. llm
            2. embedding model
            3. re rank
            4. fine tuned
        - model_format
            1. transformers
            2. sentence-transformers
            3. gguf
            4. bge-m3
    """

    model = ModelBaseSchema(
        name=name,
        description=description,
        model_provider_id=model_provider_id,
        model_type_id=model_type_id,
        model_format_id=model_format_id,
    )

    try:
        if model_provider_id == 1:  # HuggingFace
            result = HuggingFaceModelService().create(model, db)
        elif model_provider_id == 2:  # Ollama
            ...
        elif model_provider_id == 3:  # Custom
            result = CustomModelService().create(model, file, db)
        else:
            print("Error has been occured!")
        return result
    except Exception as e:
        db.rollback()
        raise e


@model_router.get("/{model_id}", response_model=ModelReadSchema)
def read_model(model_id: int, db: Session = SessionDepends):
    """
    주어진 모델 ID에 해당하는 모델을 데이터베이스에서 조회합니다.

    Args:
        model_id (int): 조회할 모델의 ID.
        db (Session): 데이터베이스 세션 객체. 기본값은 SessionDepends.

    Raises:
        HTTPException: 모델을 찾을 수 없는 경우 404 상태 코드와 함께 예외를 발생시킵니다.

    Returns:
        ModelReadSchema: 조회된 모델 객체.
    """
    db_model = ModelService().get(db, model_id)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return db_model


@model_router.get("", response_model=list[ModelReadSchema])
def read_models(skip: int = 0, limit: int = 10, db: Session = SessionDepends):
    """
    데이터베이스에서 모델 목록을 조회합니다.

    Args:
        skip (int): 조회를 건너뛸 모델 수. 기본값은 0.
        limit (int): 최대 조회할 모델 수. 기본값은 10.
        db (Session): 데이터베이스 세션 객체. 기본값은 SessionDepends.

    Returns:
        list[ModelReadSchema]: 조회된 모델 목록.
    """
    models = ModelService().get_multi(db)
    return models


@model_router.post("/{model_id}/load")
def load_model(db: Session = SessionDepends, *, model_id: int):
    """
    주어진 모델 ID에 해당하는 모델을 로드합니다.

    Args:
        model_id (int): 로드할 모델의 ID.
        db (Session): 데이터베이스 세션 객체. 기본값은 SessionDepends.

    Returns:
        str: 로드된 모델의 이름을 포함하는 메시지.
    """
    db_model = ModelService().get(db, model_id)
    model_uri = db_model.model_registry.model_uri
    loaded_pipeline = ModelService.load_transformers(model_uri)
    model = loaded_pipeline.model
    tokenizer = loaded_pipeline.tokenizer

    value = {
        "name": db_model.name,
        "model": model,
        "tokenizer": tokenizer
    }
    # TODO: 일단, llm으로 한정
    settings.add_llm(model_id, value)
    return f"{db_model.name} Loaded!",

@model_router.get("models/loaded")
def get_loaded_models(model_type: str="llm") -> dict[int, str]:
    """
    현재 로드된 모델 목록을 조회합니다.

    Args:
        model_type (str): 조회할 모델의 유형. 기본값은 "llm".

    Returns:
        dict[int, str]: 모델 ID와 모델 이름을 포함하는 딕셔너리.
    """
    result = {key: value.get("name") for key, value in settings.LOADED_LLM.items()}
    return result

@model_router.post("models/{model_id}/shutdown")
def shutdown_model(model_id: int, model_type: str="llm") -> dict[int, str]:
    """
    주어진 모델 ID에 해당하는 모델을 종료합니다.

    Args:
        model_id (int): 종료할 모델의 ID.
        model_type (str): 종료할 모델의 유형. 기본값은 "llm".

    Returns:
        dict[int, str]: 남아있는 모델 ID와 이름을 포함하는 딕셔너리.
    """
    del settings.LOADED_LLM[model_id]
    result = {key: value.get("name") for key, value in settings.LOADED_LLM.items()}
    return result