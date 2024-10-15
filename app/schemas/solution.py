from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from schemas.knowledge import KnowledgeReadSchema


class SolutionCreateSchema(BaseModel):
    solution: SolutionBaseSchema
    solution_config: SolutionConfigCreateSchema


class SolutionBaseSchema(BaseModel):
    name: str
    description: str
    knowledge_id: int


class SolutionReadSchema(BaseModel):
    id: int
    name: str
    description: str
    knowledge: KnowledgeReadSchema
    solution_config: SolutionConfigReadSchema

    class Config:
        from_attributes = True


class SolutionConfigCreateSchema(BaseModel):
    temperature: float
    presence_penalty: float
    frequency_penalty: float
    max_tokens: int
    top_p: float


class SolutionConfigBaseSchema(BaseModel):
    solution_id: int
    temperature: float
    presence_penalty: float
    frequency_penalty: float
    max_tokens: int
    top_p: float


class SolutionConfigReadSchema(BaseModel):
    id: int
    solution_id: int
    temperature: float
    presence_penalty: float
    frequency_penalty: float
    max_tokens: int
    top_p: float

    class Config:
        from_attributes = True
