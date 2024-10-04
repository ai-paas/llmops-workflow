from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PromptCreateSchema(BaseModel):
    prompt: PromptBaseSchema
    prompt_variable: None | list[str]


class PromptBaseSchema(BaseModel):
    name: str
    content: str


class PromptReadSchema(BaseModel):
    id: int
    name: str
    content: str
    prompt_variable: list[PromptVariableReadSchema] | None

    class Config:
        from_attributes = True


class PromptVariableBaseSchema(BaseModel):
    name: str
    prompt_id: int


class PromptVariableReadSchema(BaseModel):
    id: int
    name: str
    prompt_id: int

    class Config:
        from_attributes = True
