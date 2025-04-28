from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import uuid
from datetime import datetime

from schemas.apis.request import PromptCreateSchema, PromptUpdateSchema
from schemas.apis.response import PromptResponse, PromptListResponse, ResponseFormatSchema

router = APIRouter(prefix="/prompts", tags=["Prompts"])

@router.post("", response_model=ResponseFormatSchema[PromptResponse], status_code=201)
async def create_prompt(prompt: PromptCreateSchema):
    """
    새로운 프롬프트를 생성합니다.
    """
    # TODO: 실제 구현에서는 데이터베이스 저장 로직 추가
    prompt_id = str(uuid.uuid4())
    
    # TODO: 프롬프트 저장 로직 구현
    prompt_data = {
        "id": prompt_id,
        "name": prompt.name,
        "description": prompt.description,
        "content": prompt.content,
        "variables": [var.model_dump() for var in prompt.variables],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    return ResponseFormatSchema(
        status=201,
        message="Prompt created successfully",
        pagination=None,
        data=prompt_data
    )

@router.get("", response_model=ResponseFormatSchema[PromptListResponse])
async def list_prompts(
    skip: int = Query(0, description="건너뛸 항목 수"),
    limit: int = Query(10, description="가져올 항목 수"),
    search: Optional[str] = Query(None, description="검색어")
):
    """
    프롬프트 목록을 조회합니다.
    """
    # TODO: 실제 구현에서는 데이터베이스 조회 로직 추가
    return ResponseFormatSchema(
        status=200,
        message="Prompts retrieved successfully",
        pagination={"skip": skip, "limit": limit, "total": 0},
        data={"total": 0, "prompts": []}
    )

@router.get("/{prompt_id}", response_model=ResponseFormatSchema[PromptResponse])
async def get_prompt(prompt_id: str):
    """
    특정 프롬프트의 상세 정보를 조회합니다.
    """
    # TODO: 실제 구현에서는 데이터베이스 조회 로직 추가
    raise HTTPException(status_code=404, detail="Prompt not found")

@router.put("/{prompt_id}", response_model=ResponseFormatSchema[PromptResponse])
async def update_prompt(prompt_id: str, prompt: PromptUpdateSchema):
    """
    특정 프롬프트의 정보를 수정합니다.
    """
    # TODO: 실제 구현에서는 데이터베이스 업데이트 로직 추가
    raise HTTPException(status_code=404, detail="Prompt not found")

@router.delete("/{prompt_id}", response_model=ResponseFormatSchema)
async def delete_prompt(prompt_id: str):
    """
    특정 프롬프트를 삭제합니다.
    """
    # TODO: 실제 구현에서는 데이터베이스 삭제 로직 추가
    raise HTTPException(status_code=404, detail="Prompt not found") 