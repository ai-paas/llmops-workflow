from typing import Any

from llama_cpp import Llama
from services.mlflow_service import GgufRegistry, TransformersRegistry
from services.model_service.base import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer


class HuggingFaceLlm(BaseModel):
    def __init__(self):
        ...

    def register_to_mlflow(self, model_name: str, *, file_name: str = None):
        if file_name is None:
            registry = TransformersRegistry()
            model = self._load_transformers(model_name)
        else:
            registry = GgufRegistry()
            model = self._load_gguf(model_name, file_name=file_name)
        return registry.register(model, model_name)

    def _load_transformers(self, model_name: str) -> dict[str, Any]:
        """
        transformers 계열 Model을 Load하는 method

        * params
            * repo: str
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
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        return {
            "model": model,
            "tokenizer": tokenizer,
        }

    def _load_gguf(self, model_name: str, file_name: str):
        """
        Huggingface Llama.cpp 계열 gguf Model을 등록하는 method

        * params
            * model_name: repo_id (e.g. "google/gemma-2-2b-it-GGUF")
            * file_name: gguf file name (e.g. "2b_it_v2.gguf")
        """
        return Llama.from_pretrained(repo_id=model_name, filename=file_name, verbose=False)


class UserUploadLlm(BaseModel):
    def register_to_mlflow(self):
        # HuggingFace에서 임베딩 모델 로드 및 MLflow에 업로드
        print("HuggingFace 임베딩 모델을 MLflow에 업로드합니다.")
        # MLFlowService.upload_model(...)

    def _load_transformers(self):
        ...

    def _load_gguf(self, model_path: str):
        """
        Llama.cpp 계열 gguf Model을 등록하는 method

        * params
            * model_path: gguf file path (e.g. "your/model/file/path.gguf")
        """
        # TODO: 기타 parameter 체크
        return Llama(
            model_path=model_path,
            # n_gpu_layers=-1, # Uncomment to use GPU acceleration
            # seed=1337, # Uncomment to set a specific seed
            # n_ctx=2048, # Uncomment to increase the context window
        )
