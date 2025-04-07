from datetime import datetime
from typing import Annotated
from urllib.parse import quote

from config.db.connect import SessionDepends
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from schemas.evaluation import RetrievalRequestSchema, RetrievalResponseSchema
from services.evaluation_service import EvaluationService
from sqlalchemy.orm import Session

evaluation_router = APIRouter(prefix="/evaluations", tags=["Evaluations"])


@evaluation_router.post("/retrieval", response_model=list[RetrievalResponseSchema])
def retrieve(request: RetrievalRequestSchema, db: Session = SessionDepends):
    return EvaluationService().retrieve(request, db)
