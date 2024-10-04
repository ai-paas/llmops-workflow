from datetime import datetime
from typing import Annotated
from urllib.parse import quote

from config.db.connect import SessionDepends
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from schemas.knowledge import (
    KnowledgeBaseSchema,
    KnowledgeFileBaseSchema,
    KnowledgeFileReadSchema,
    KnowledgeReadSchema,
)
from services.knowledge_service import KnowledgeDatasetService, KnowledgeService
from sqlalchemy.orm import Session

knowledge_router = APIRouter(prefix="/knowledges", tags=["Knowledges"])


@knowledge_router.post("", response_model=KnowledgeReadSchema)
def create_knowledge(knowledge_base: KnowledgeBaseSchema, db: Session = SessionDepends):
    """
    지식 정보를 생성하는 함수.

    Args:
        knowledge_base (KnowledgeBaseSchema): 생성할 지식 정보 스키마.
        db (Session): 데이터베이스 세션. 기본적으로 SessionDepends로 주입됨.

    Returns:
        KnowledgeReadSchema: 생성된 지식 정보의 스키마를 반환.

    Raises:
        Exception: 지식 정보를 생성하는 동안 발생한 예외.
    """
    try:
        result = KnowledgeService().create(db, knowledge_base)
        db.commit()
        return result
    except Exception:
        raise ("Error has been Occured!")


@knowledge_router.put("/{knowledge_id}", response_model=KnowledgeReadSchema)
def update_knowledge(knowledge_id: int, knowledge_base: KnowledgeBaseSchema, db: Session = SessionDepends):
    """
    지식 정보를 수정하는 함수.

    Args:
        knowledge_base (KnowledgeBaseSchema): 생성할 지식 정보 스키마.
        db (Session): 데이터베이스 세션. 기본적으로 SessionDepends로 주입됨.

    Returns:
        KnowledgeReadSchema: 생성된 지식 정보의 스키마를 반환.

    Raises:
        Exception: 지식 정보를 생성하는 동안 발생한 예외.
    """
    try:
        knowledge_service = KnowledgeService()
        db_obj = knowledge_service.get(db, knowledge_id)
        result = knowledge_service.update(db, db_obj, knowledge_base)
        db.commit()
        return result
    except Exception:
        raise ("Error has been Occured!")


@knowledge_router.get("", response_model=list[KnowledgeReadSchema])
def get_multi_knowledge(db: Session = SessionDepends):
    """
    여러 지식 정보를 조회하는 함수.

    Args:
        db (Session): 데이터베이스 세션. 기본적으로 SessionDepends로 주입됨.

    Returns:
        list[KnowledgeReadSchema]: 데이터베이스에서 조회한 여러 지식 정보 스키마의 리스트를 반환.
    """
    return KnowledgeService().get_multi(db)


@knowledge_router.get("/{knowledge_id}", response_model=KnowledgeReadSchema)
def get_knowledge(knowledge_id: int, *, db: Session = SessionDepends):
    """
    특정 ID를 기준으로 지식 정보를 조회하는 함수.

    Args:
        knowledge_id (int): 조회할 지식 정보의 ID.
        db (Session): 데이터베이스 세션. 기본적으로 SessionDepends로 주입됨.

    Returns:
        KnowledgeReadSchema: ID에 해당하는 지식 정보 스키마를 반환.
    """
    return KnowledgeService().get(db, pk=knowledge_id)


@knowledge_router.post("/{knowledge_id}/datasets", response_model=KnowledgeFileReadSchema)
def create_knowledge_dataset(knowledge_id: int, file: Annotated[UploadFile, File()], *, db: Session = SessionDepends):
    """
    주어진 지식 항목(knowledge)에 새로운 데이터셋을 생성합니다.

    이 엔드포인트는 사용자가 파일을 업로드하고, 해당 파일을 특정 지식 항목에 연결할 수 있게 합니다.
    업로드된 파일은 처리되어 시스템에 저장되며, 파일의 메타데이터는 데이터베이스에 저장됩니다.

    Args:
        knowledge_id (int): 데이터셋이 연결될 지식 항목의 ID.
        file (UploadFile): 업로드할 파일 (`multipart/form-data` 형식).
        db (Session): 데이터베이스 세션으로, 데이터베이스 작업에 사용됩니다.

    Returns:
        KnowledgeFileReadSchema: 생성된 지식 데이터셋에 대한 메타데이터를 반환합니다.
    """
    return KnowledgeDatasetService().create_dataset(knowledge_id, file, db)


@knowledge_router.get("/{knowledge_id}/datasets/download")
async def download_dataset(knowledge_id: int, path: str, db: Session = SessionDepends):
    """
    주어진 지식 항목과 연결된 파일을 다운로드합니다.

    이 엔드포인트는 사용자가 특정 지식 항목에 연결된 파일을 다운로드할 수 있도록 합니다.
    사용자는 파일 경로와 지식 ID를 제공하여 파일을 다운로드할 수 있습니다.

    Args:
        knowledge_id (int): 다운로드할 파일이 연결된 지식 항목의 ID.
        path (str): 다운로드할 파일의 경로 (버킷 및 파일명 포함).
        db (Session): 데이터베이스 세션으로, 데이터베이스 작업에 사용됩니다.

    Returns:
        StreamingResponse: 사용자가 다운로드할 수 있는 파일 스트림을 반환합니다.
    """
    # TODO: 하드코딩 제거
    bucket_name = "gen_ai_solution"
    file_stream = KnowledgeDatasetService.get_file_object(bucket_name, path)
    _, file_name = path.split("/")
    file_name = quote(file_name)
    headers = {
        "Content-Disposition": f"attachment; filename*=UTF-8''{file_name}",
    }
    return StreamingResponse(file_stream, media_type="application/octet-stream", headers=headers)
