from services.model_service.base import BaseModel


class HuggingFaceEmbeddingModel(BaseModel):
    def upload_to_mlflow(self):
        # HuggingFace에서 임베딩 모델 로드 및 MLflow에 업로드
        print("HuggingFace 임베딩 모델을 MLflow에 업로드합니다.")
        # MLFlowService.upload_model(...)


class UserUploadEmbeddingModel(BaseModel):
    def upload_to_mlflow(self):
        # HuggingFace에서 임베딩 모델 로드 및 MLflow에 업로드
        print("HuggingFace 임베딩 모델을 MLflow에 업로드합니다.")
        # MLFlowService.upload_model(...)
