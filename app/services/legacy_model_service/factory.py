from abc import ABC, abstractclassmethod

from services.model_service.base import BaseModel
from services.model_service.embedding import (
    HuggingFaceEmbeddingModel,
    UserUploadEmbeddingModel,
)
from services.model_service.llm import HuggingFaceLlm, UserUploadLlm


class AbstractFactory(ABC):
    """Model(LLM, Embedding Model) 공급 주체에 따라, 분기하는 추상 팩토리 Class"""

    @abstractclassmethod
    def create_llm(self) -> BaseModel:
        ...

    @abstractclassmethod
    def create_embedding_model(self) -> BaseModel:
        ...


class HuggingFaceFactory(AbstractFactory):
    """Pulling model from HuggingFace"""

    @staticmethod
    def create_llm() -> BaseModel:
        return HuggingFaceLlm()

    def create_embedding_model() -> BaseModel:
        return HuggingFaceEmbeddingModel()


class UploadFactory(AbstractFactory):
    """Upload Models by users"""

    @staticmethod
    def create_llm() -> BaseModel:
        return UserUploadLlm()

    @staticmethod
    def create_embedding_model() -> BaseModel:
        return UserUploadEmbeddingModel()


def get_model_factory(provider_id: int, model_type: int) -> BaseModel:
    provider = HuggingFaceFactory if provider_id == 3 else UploadFactory
    if model_type == 3:
        return provider.create_llm()
    elif model_type == 4:
        return provider.create_embedding_model()
    else:
        HTTPException(status_code=400, detail="잘못된 Model Type 입니다!")
