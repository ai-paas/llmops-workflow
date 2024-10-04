from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from schemas.model import ModelReadSchema


class KnowledgeBaseSchema(BaseModel):
    name: str
    display_name: str
    description: str
    permission_id: int
    language_id: int
    model_id: int
    search_type_id: int
    chunk_type_id: int
    top_k: int
    score: float
    chunk_length: int
    overlap: int


class KnowledgeReadSchema(BaseModel):
    id: int
    name: str
    display_name: str
    description: str
    permission: PermissionReadSchema
    language: LanguageReadSchema
    # TODO: Model sentence transformer 개발 후 수정
    # model: ModelRead
    search_type: SearchTypeReadSchema
    top_k: int
    score: float
    chunk_length: int
    overlap: int
    chunk_type: ChunkTypeReadSchema
    dataset: list[KnowledgeFileReadSchema] | None

    class Config:
        from_attributes = True


class PermissionReadSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class LanguageReadSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class SearchTypeReadSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class KnowledgeFileBaseSchema(BaseModel):
    name: str
    path: str
    knowledge_id: int
    file_type: str
    chunk_number: int


class KnowledgeFileReadSchema(BaseModel):
    id: int
    name: str
    path: str
    knowledge_id: int
    file_type: str
    chunk_number: int
    created_by: str
    created_at: datetime | None
    updated_by: str
    updated_at: datetime | None

    class Config:
        from_attributes = True


class FileTypeReadSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class ChunkTypeReadSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
