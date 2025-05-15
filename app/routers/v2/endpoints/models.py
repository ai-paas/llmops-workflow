from fastapi import APIRouter, UploadFile, File, Form
from typing import Annotated, Optional
from sqlalchemy.orm import Session

from schemas.apis.request import ModelCreateSchema
from schemas.apis.response import ModelResponseSchema, ResponseFormatSchema
from config.db.connect import SessionDepends
from services.model_service import ModelService

router = APIRouter(prefix="/models", tags=["Models"])


@router.post("", response_model=ResponseFormatSchema[ModelResponseSchema], status_code=201)
async def create_model(
    *,
    db: Session = SessionDepends,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    model_provider_id: Annotated[int, Form()],
    model_type_id: Annotated[int, Form()],
    model_format_id: Annotated[int, Form()],
    model_file: UploadFile | None = None,
):
    """
    새로운 모델을 생성하고 MLflow 레지스트리에 등록합니다.
    
    모델 정보를 데이터베이스에 저장하고, 모델 유형에 따라 적절한 MLflow 레지스트리에 등록합니다.
    모델 제공자(HuggingFace, Ollama, Custom)와 모델 형식(Transformers, Sentence-Transformers, GGUF, BGE-M3)에 
    따라 다른 로직으로 처리됩니다.
    
    Args:
        db (Session): 데이터베이스 세션 객체
        model (ModelCreateSchema): 생성할 모델의 정보
            - name: 모델 이름
            - description: 모델 설명
            - model_provider_id: 모델 제공자 ID (1: HuggingFace, 2: Ollama, 3: Custom)
            - model_type_id: 모델 타입 ID (1: LLM, 2: Embedding, 3: Re-Rank, 4: Fine-Tuned)
            - model_format_id: 모델 포맷 ID (1: Transformers, 2: Sentence-Transformers, 3: GGUF, 4: BGE-M3)
        model_file (Optional[UploadFile]): Custom 모델인 경우 업로드할 모델 파일 (GGUF 형식)
        
    Returns:
        ResponseFormatSchema[ModelResponseSchema]: 생성된 모델 정보와 응답 상태를 포함한 응답 객체
            - status: HTTP 상태 코드 (201)
            - message: 응답 메시지
            - data: 생성된 모델 정보
        
    Raises:
        HTTPException: 모델 생성 중 오류가 발생한 경우 (지원하지 않는 모델 형식, 파일 업로드 실패 등)
        ValueError: 지원하지 않는 모델 형식이 제공된 경우
    """
    model = ModelCreateSchema(
        name=name,
        description=description,
        model_provider_id=model_provider_id,
        model_type_id=model_type_id,
        model_format_id=model_format_id,
    )
    
    result = ModelService().create_model(db, model)
    
    return ResponseFormatSchema(
        status=201,
        pagination=None,
        message="Model created successfully",
        data=result
    )
