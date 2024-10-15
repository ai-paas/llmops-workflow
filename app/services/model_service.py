import tempfile
from typing import Any

from fastapi import UploadFile
from FlagEmbedding import BGEM3FlagModel
from llama_cpp import Llama
from repos.model import model_registry_repository, model_repository
from schemas.model import (
    ModelBaseSchema,
    ModelReadSchema,
    ModelRegistryBaseSchema,
    ModelRegistryReadSchema,
)
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer, pipeline
from util.model_registry import ModelLoader, ModelRegistry


class ModelService:
    def get(self, db: Session, pk: int) -> ModelReadSchema:
        return model_repository.get(db, pk)

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> list[ModelReadSchema]:
        return model_repository.get_multi(db, skip=skip, limit=limit)

    def get_all(self, db: Session) -> list[ModelReadSchema]:
        return model_repository.get_all(db)

    def update(self, db: Session, db_obj, obj_in):
        return model_repository.update(db, db_obj=db_obj, obj_in=obj_in)

    def validate(self, model_format_id: int, model_uri: str) -> str:
        # TODO: model_format_id로부터 get 하도록 변경
        if model_format_id == 1:
            pipeline = ModelLoader.load_transformers(model_uri)
            messages = [
                {"role": "user", "content": "Who are you?"},
            ]
            result = pipeline(messages, max_length=1024)
        elif model_format_id == 3:
            loaded_model = ModelLoader.load_pyfunc(model_uri)
            messages = [
                {"role": "user", "message": "Where is the capital of Korea?"},
            ]
            result = loaded_model.predict(messages)
            print(result)
        else:
            result = ""
        return result

    staticmethod
    def load_transformers(model_uri: str):
        loaded_pipe = ModelLoader.load_transformers(model_uri)
        return loaded_pipe


class HuggingFaceModelService:
    def create(self, model_schema: ModelBaseSchema, db: Session):
        model_format_id = model_schema.model_format_id
        repo_id = model_schema.name
        # TODO: model_format_id로부터 get 하도록 변경
        if model_format_id == 1:  # transformers
            model = self.load_transformers(repo_id)
            run_id, artifact_uri, model_version, model_uri = ModelRegistry().log_transformers(model, repo_id)
        elif model_format_id == 2:  # sentence-transformers
            model = self.load_sentence_transformers(repo_id)
            run_id, artifact_uri, model_version, model_uri = ModelRegistry().log_sentence_transformers(model, repo_id)
        elif model_format_id == 3:  # gguf
            # TODO: 하드코딩 제거
            model = self.load_gguf(repo_id, "gemma-2-2b-it.Q8_0.gguf")
            run_id, artifact_uri, model_version, model_uri = ModelRegistry().log_pyfunc(model, repo_id)
        elif model_format_id == 4:  # bge m3
            model = self.load_bgem3flag(repo_id)
            run_id, artifact_uri, model_version, model_uri = ModelRegistry().log_pyfunc(model, repo_id)
        else:
            print("Error!!!")

        model_obj = model_repository.create(db, obj_in=model_schema)
        model_id = model_obj.id
        model_registry_obj = model_registry_repository.create(
            db,
            obj_in=ModelRegistryBaseSchema(
                run_id=run_id, version=model_version, artifact_path=artifact_uri, model_uri=model_uri, model_id=model_id
            ),
        )
        db.commit()
        return model_repository.get(db, model_id)

    @staticmethod
    def load_transformers(repo_id: str) -> dict[str, Any]:
        """
        transformers 계열 Model을 Load하는 method

        * params
            * repo_id: str
                - from HuggingFace: model_name (e.g. 'openbmb/MiniCPM-V-2_6-gguf')
                - from User: Model과 Tokenizer가 함께 저장된 directory 경로

        * return
            - transformer_model used in mlflow.transformers.log_model
                ```python
                components = {
                    "model": model,
                    "tokenizer": tokenizer,
                }
                ```
        """
        # TODO: MS 제공 Model의 경우, trust_remote_code=True 옵션을 추가해야하는 경우 발견됨
        tokenizer = AutoTokenizer.from_pretrained(repo_id)
        model = AutoModelForCausalLM.from_pretrained(repo_id)
        return {
            "model": model,
            "tokenizer": tokenizer,
        }

    @staticmethod
    def load_sentence_transformers(repo_id: str) -> SentenceTransformer:
        model = SentenceTransformer(repo_id)
        return model

    @staticmethod
    def load_gguf(repo_id: str, file_name: str) -> Llama:
        """
        Huggingface Llama.cpp 계열 gguf Model을 등록하는 method

        * params
            * repo_id: e.g. "google/gemma-2-2b-it-GGUF"
            * file_name: gguf file name (e.g. "2b_it_v2.gguf")
        """
        return Llama.from_pretrained(repo_id=repo_id, filename=file_name, verbose=False)

    @staticmethod
    def load_bgem3flag(repo_id: str) -> BGEM3FlagModel:
        model = BGEM3FlagModel(repo_id, use_fp16=False)
        return model


class OllamaModelService:
    """
    Ollama에 Model을 저장하고 불러오는 service
    """

    ...


class CustomModelService:
    """
    Llama.cpp 계열 gguf Model을 등록하는 method

    * params
        * model_path: gguf file path (e.g. "your/model/file/path.gguf")
    """

    def create(self, model_schema: ModelBaseSchema, file: UploadFile, db: Session):
        model_format_id = model_schema.model_format_id

        if not model_format_id == 3:
            return "Unsupported type!"

        contents = file.file.read()
        model_name = model_schema.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".gguf") as temp_file:
            temp_file.write(contents)
            temp_file_path = temp_file.name
            model = Llama(model_path=temp_file_path)
            run_id, artifact_uri, model_version, model_uri = ModelRegistry().log_llamacpp(model, model_name)

        model_obj = model_repository.create(db, obj_in=model_schema)
        model_id = model_obj.id
        model_registry_obj = model_registry_repository.create(
            db,
            obj_in=ModelRegistryBaseSchema(
                run_id=run_id, version=model_version, artifact_path=artifact_uri, model_uri=model_uri, model_id=model_id
            ),
        )
        db.commit()
        return model_repository.get(db, model_id)
