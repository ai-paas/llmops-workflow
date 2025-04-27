from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form
from typing import Optional
import uuid
from datetime import datetime

from schemas.apis.request import (
    DatasetCreateSchema, 
    DatasetUpdateSchema,
    DatasetFileAddSchema
)
from schemas.apis.response import (
    DatasetResponse, 
    DatasetListResponse, 
    DatasetFileResponse,
    DatasetFileListResponse,
    ResponseFormatSchema
)

router = APIRouter(prefix="/datasets", tags=["Datasets"])

@router.post("", response_model=ResponseFormatSchema[DatasetResponse], status_code=201)
async def create_dataset(
    dataset: DatasetCreateSchema = Form(...),
    file: UploadFile = File(...)
):
    """
    새로운 데이터셋을 생성합니다.
    지원하는 파일 형식: .txt, .md, .mdx, .pdf, .html, .xlsx, .xls, .docx, .csv, .htm
    """
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="File is required")
        
    # 파일 확장자 검증
    allowed_extensions = {'.txt', '.md', '.mdx', '.pdf', '.html', '.xlsx', '.xls', '.docx', '.csv', '.htm'}
    file_extension = file.filename[file.filename.rfind('.'):].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Allowed formats: {', '.join(allowed_extensions)}"
        )
    
    # TODO: 실제 구현에서는 파일 저장 및 데이터셋 정보 저장 로직 추가
    dataset_id = str(uuid.uuid4())
    file_path = f"datasets/{dataset_id}/{file.filename}"
    
    dataset_data = {
        "id": dataset_id,
        "basic_info": dataset.basic_info.model_dump(),
        "chunk_settings": dataset.chunk_settings.model_dump(),
        "embedding_settings": dataset.embedding_settings.model_dump(),
        "search_settings": dataset.search_settings.model_dump(),
        "file_path": file_path,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    return ResponseFormatSchema(
        status=201,
        message="Dataset created successfully",
        pagination=None,
        data=dataset_data
    )

@router.post("/{dataset_id}/files", response_model=ResponseFormatSchema[DatasetFileResponse], status_code=201)
async def add_file_to_dataset(
    dataset_id: str,
    file: UploadFile = File(...),
    file_info: DatasetFileAddSchema = Form(...)
):
    """
    기존 데이터셋에 파일을 추가합니다.
    지원하는 파일 형식: .txt, .md, .mdx, .pdf, .html, .xlsx, .xls, .docx, .csv, .htm
    """
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="File is required")
        
    # 파일 확장자 검증
    allowed_extensions = {'.txt', '.md', '.mdx', '.pdf', '.html', '.xlsx', '.xls', '.docx', '.csv', '.htm'}
    file_extension = file.filename[file.filename.rfind('.'):].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Allowed formats: {', '.join(allowed_extensions)}"
        )
    
    # TODO: 실제 구현에서는 데이터셋 존재 여부 확인 및 파일 저장 로직 추가
    file_id = str(uuid.uuid4())
    file_path = f"datasets/{dataset_id}/files/{file_id}/{file.filename}"
    
    file_data = {
        "id": file_id,
        "dataset_id": dataset_id,
        "filename": file.filename,
        "file_path": file_path,
        "description": file_info.description,
        "created_at": datetime.now()
    }
    
    return ResponseFormatSchema(
        status=201,
        message="File added to dataset successfully",
        pagination=None,
        data=file_data
    )

@router.get("/{dataset_id}/files", response_model=ResponseFormatSchema[DatasetFileListResponse])
async def list_dataset_files(
    dataset_id: str,
    skip: int = Query(0, description="건너뛸 항목 수"),
    limit: int = Query(10, description="가져올 항목 수")
):
    """
    데이터셋에 포함된 파일 목록을 조회합니다.
    """
    # TODO: 실제 구현에서는 데이터베이스 조회 로직 추가
    return ResponseFormatSchema(
        status=200,
        message="Dataset files retrieved successfully",
        pagination={"skip": skip, "limit": limit, "total": 0},
        data={"total": 0, "files": []}
    )

@router.delete("/{dataset_id}/files/{file_id}", response_model=ResponseFormatSchema)
async def delete_dataset_file(dataset_id: str, file_id: str):
    """
    데이터셋에서 특정 파일을 삭제합니다.
    """
    # TODO: 실제 구현에서는 데이터베이스 삭제 및 파일 삭제 로직 추가
    raise HTTPException(status_code=404, detail="File not found")

@router.get("", response_model=ResponseFormatSchema[DatasetListResponse])
async def list_datasets(
    skip: int = Query(0, description="건너뛸 항목 수"),
    limit: int = Query(10, description="가져올 항목 수"),
    search: Optional[str] = Query(None, description="검색어")
):
    """
    데이터셋 목록을 조회합니다.
    """
    # TODO: 실제 구현에서는 데이터베이스 조회 로직 추가
    return ResponseFormatSchema(
        status=200,
        message="Datasets retrieved successfully",
        pagination={"skip": skip, "limit": limit, "total": 0},
        data={"total": 0, "datasets": []}
    )

@router.get("/{dataset_id}", response_model=ResponseFormatSchema[DatasetResponse])
async def get_dataset(dataset_id: str):
    """
    특정 데이터셋의 상세 정보를 조회합니다.
    """
    # TODO: 실제 구현에서는 데이터베이스 조회 로직 추가
    raise HTTPException(status_code=404, detail="Dataset not found")

@router.put("/{dataset_id}", response_model=ResponseFormatSchema[DatasetResponse])
async def update_dataset(
    dataset_id: str,
    dataset: DatasetUpdateSchema = Form(...),
    file: Optional[UploadFile] = File(None)
):
    """
    특정 데이터셋의 정보를 수정합니다.
    파일을 업로드할 수 있습니다.
    """
    # TODO: 실제 구현에서는 데이터베이스 업데이트 및 파일 저장 로직 추가
    raise HTTPException(status_code=404, detail="Dataset not found")

@router.delete("/{dataset_id}", response_model=ResponseFormatSchema)
async def delete_dataset(dataset_id: str):
    """
    특정 데이터셋을 삭제합니다.
    """
    # TODO: 실제 구현에서는 데이터베이스 삭제 및 파일 삭제 로직 추가
    raise HTTPException(status_code=404, detail="Dataset not found")
