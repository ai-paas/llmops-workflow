from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RetrievalRequestSchema(BaseModel):
    query: str
    knowledge_id: int
    search_type_id: int
    top_k: int
    threshold_score: float


class RetrievalResponseSchema(BaseModel):
    distance: float
    text: str
