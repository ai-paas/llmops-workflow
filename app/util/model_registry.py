import os
from typing import Any

import mlflow
from config.settings import get_settings
from mlflow import MlflowClient
from mlflow.models import ModelSignature, infer_signature
from mlflow.pyfunc import PythonModel
from FlagEmbedding import BGEM3FlagModel

settings = get_settings()

# 환경 변수를 통한 타임아웃 설정
os.environ["MLFLOW_HTTP_REQUEST_TIMEOUT"] = "300"  # 5분으로 설정


con = {
    "name": "mlflow-env",
    "channels": ["conda-forge"],
    "dependencies": [
        "python=3.9",
        {
            "pip": ["llama-cpp-python"],
        },
    ],
}


class ModelRegistry:
    def __init__(self):
        self._client = MlflowClient(tracking_uri=settings.MLFLOW_TRACKING_URI)
        self._experiment_name = settings.MLFLOW_EXPERIMENT_NAME
        experiment = mlflow.get_experiment_by_name(self._experiment_name)
        if experiment == None:
            mlflow.create_experiment(self._experiment_name)

    def log_transformers(self, model: dict[str, Any], model_name: str):
        """
        Private Model을 Model Repository에 저장하는 method

        * Parmas
            * repo: Model 공급 유형에 따라 달라짐
                - Huggingface transfromers : repo_id
                - Huggingface gguf : repo_id, file_name
        """
        mlflow.set_experiment(self._experiment_name)
        with mlflow.start_run(run_name=model_name) as run:
            model_name = model_name.replace("/", "-")
            mlflow.transformers.log_model(
                transformers_model=model,
                artifact_path=model_name,
                registered_model_name=model_name,
            )

            run_id = run.info.run_id
            artifact_uri = mlflow.get_artifact_uri()
            model_version = self._client.get_latest_versions(name=model_name, stages=["None"])[0].version
            model_uri = f"models:/{model_name}/{model_version}"
        return run_id, artifact_uri, model_version, model_uri

    def log_sentence_transformers(self, model, model_name: str):
        mlflow.set_experiment(self._experiment_name)

        data = "This is a test data!"
        signature = mlflow.models.infer_signature(
            model_input=data,
            model_output=model.encode(data),
        )
        with mlflow.start_run(run_name=model_name) as run:
            model_name = model_name.replace("/", "-")
            mlflow.sentence_transformers.log_model(
                model=model,
                artifact_path=model_name,
                signature=signature,
                input_example=data,
            )

            run_id = run.info.run_id
            artifact_uri = mlflow.get_artifact_uri()
            model_version = self._client.get_latest_versions(name=model_name, stages=["None"])[0].version
            model_uri = f"models:/{model_name}/{model_version}"
        return run_id, artifact_uri, model_version, model_uri

    def log_pyfunc(self, model, model_name: str):
        """
        Private Model을 Model Repository에 저장하는 method

        gguf, BGEMeEmbedding 등 mlflow flavor에 정의되어 있지 않은 것을 등록
        """
        mlflow.set_experiment(self._experiment_name)
        with mlflow.start_run(run_name=model_name) as run:
            model_name = model_name.replace("/", "-")
            mlflow.pyfunc.log_model(
                artifact_path=model_name, python_model=PyfuncModelWrapper(model), registered_model_name=model_name
            )
            run_id = run.info.run_id
            artifact_uri = mlflow.get_artifact_uri()
            model_version = self._client.get_latest_versions(name=model_name, stages=["None"])[0].version
            model_uri = f"models:/{model_name}/{model_version}"
        return run_id, artifact_uri, model_version, model_uri

    def log_llamacpp(self, model, model_name: str):
        """
        Private Model을 Model Repository에 저장하는 method

        gguf, BGEMeEmbedding 등 mlflow flavor에 정의되어 있지 않은 것을 등록
        """
        mlflow.set_experiment(self._experiment_name)
        with mlflow.start_run(run_name=model_name) as run:
            model_name = model_name.replace("/", "-")
            mlflow.pyfunc.log_model(
                artifact_path=model_name, python_model=LlamaCppWrapper(model), registered_model_name=model_name
            )
            run_id = run.info.run_id
            artifact_uri = mlflow.get_artifact_uri()
            model_version = self._client.get_latest_versions(name=model_name, stages=["None"])[0].version
            model_uri = f"models:/{model_name}/{model_version}"
        return run_id, artifact_uri, model_version, model_uri


    def log_bge_embedding(self, model_name: str="BAAI/bge-m3"):
        mlflow.set_experiment(self._experiment_name)
        with mlflow.start_run(run_name=model_name) as run:
            repo_id = model_name
            model_name = model_name.replace("/", "-")
            mlflow.pyfunc.log_model(
                artifact_path=model_name,
                python_model=BGEEmbeddingWrapper(repo_id),
                registered_model_name=model_name
            )
            run_id = run.info.run_id
            artifact_uri = mlflow.get_artifact_uri()
            model_version = self._client.get_latest_versions(name=model_name, stages=["None"])[0].version
            model_uri = f"models:/{model_name}/{model_version}"
        return run_id, artifact_uri, model_version, model_uri



class ModelLoader:
    @staticmethod
    def load_transformers(model_uri: str):
        return mlflow.transformers.load_model(model_uri)

    @staticmethod
    def load_sentence_transformers(model_uri: str):
        return mlflow.sentence_transformers.load_model(model_uri)

    @staticmethod
    def load_pyfunc(model_uri: str):
        return mlflow.pyfunc.load_model(model_uri)


class PyfuncModelWrapper(PythonModel):
    def __init__(self, model):
        self.model = model

    def predict(self, context, model_input):
        if self.model is None:
            raise ValueError("The model has not been loaded. " "Ensure that 'load_context' is properly executed.")
        return self.model


class BGEEmbeddingWrapper(PythonModel):
    def __init__(self, repo_id: str):
        self.model = BGEM3FlagModel(repo_id, use_fp16=False)

    def predict(self, context, model_input: list[str]):
        if self.model is None:
            raise ValueError(
                "The model has not been loaded. "
                "Ensure that 'load_context' is properly executed."
            )
        return self.model.encode(
            model_input,
            batch_size=12,
            max_length=8192,
            return_dense=True,
            return_sparse=True,
            return_colbert_vecs=False,
        )


class LlamaCppWrapper(PythonModel):
    def __init__(self, model):
        self.model = model

    def predict(self, context, model_input: list[dict[str, str]]):
        return self.predict_plus(model_input)

    def predict_plus(self, model_input: list[dict[str, str]]):
        default_system = "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, \
         while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous,\
        or illegal content. Please ensure that your responses are socially unbiased and positive in nature."
        params = {"max_tokens": 50, "verbose": True}
        # max_tokens와 verbose를 처리할 때 params가 없을 수도 있다는 가정 하에 안전하게 처리합니다.
        max_tokens = int(params["max_tokens"]) if params and "max_tokens" in params else 32
        verbose = True if params and "verbose" in params else False

        # 모델 입력에 대해 프롬프트 생성
        prompt = ""
        for index, row in enumerate(model_input):
            if index == 0:
                if row["role"] == "system":
                    prompt = f"<s>[INST] <<SYS>>\n{row['message']}\n\n<</SYS>>\n\n"
                else:
                    prompt = f"<s>[INST] <<SYS>>\n{default_system}\n\n<</SYS>>\n\n"
                    if row["role"] == "user":
                        prompt += f"{row['message']} [/INST]"
                continue
            if row["role"] == "user":
                prompt += f"<s>[INST] {row['message']} [/INST]"
            elif row["role"] == "assistant":
                prompt += f" {row['message']} </s>"

        # verbose 모드일 경우 생성된 prompt를 출력
        if verbose:
            print(f"Final Prompt: {prompt}", flush=True)

        # LlamaCPP 모델을 사용해 예측 수행
        output = self.model(prompt, max_tokens=max_tokens, stop=[], echo=False)
        return output
