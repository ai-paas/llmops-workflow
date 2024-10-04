from abc import ABC, abstractmethod
from typing import Any

import mlflow
from config.settings import get_settings
from llama_cpp import Llama
from mlflow import MlflowClient
from mlflow.pyfunc import PythonModel
from schemas.model import ModelRegistryCreate

settings = get_settings()


class AbstractFactory(ABC):
    def __init__(self):
        self._client = MlflowClient(tracking_uri=settings.MLFLOW_TRACKING_URI)
        self._experiment_name = settings.MLFLOW_EXPERIMENT_NAME
        experiment = mlflow.get_experiment_by_name(self._experiment_name)
        if experiment == None:
            mlflow.create_experiment(self._experiment_name)

    @abstractmethod
    def register(self, model):
        ...

    def _get_run_info(self, run_id: str, model_name: str) -> ModelRegistryCreate:
        artifact_uri = mlflow.get_artifact_uri()
        client = mlflow.tracking.MlflowClient()
        model_version = client.get_latest_versions(name=model_name, stages=["None"])[0].version
        model_uri = f"models:/{model_name}/{model_version}"
        return ModelRegistryCreate(
            run_id=run_id, model_name=model_name, version=model_version, artifact_path=artifact_uri, model_uri=model_uri
        )
        # return run_id, artifact_uri, model_name, model_version, model_uri


class TransformersRegistry(AbstractFactory):
    def register(self, model: dict[str, Any], model_name: str) -> ModelRegistryCreate:
        """
        Private Model을 Model Repository에 저장하는 method

        * Parmas
            * repo: Model 공급 유형에 따라 달라짐
                - Huggingface transfromers : repo_id
                - Huggingface gguf : repo_id, file_name
        """
        mlflow.set_experiment(self._experiment_name)
        model_name = model_name.replace("/", "-")
        with mlflow.start_run() as run:
            mlflow.transformers.log_model(
                transformers_model=model,
                artifact_path=model_name,
                registered_model_name=model_name,
            )
            run_info = self._get_run_info(run.info.run_id, model_name)
        return run_info
        # model_uri = f"models:/{model_name}/latest"
        # loaded_model = mlflow.transformers.load_model(model_uri)
        # model = loaded_model.model
        # tokenizer = loaded_model.tokenizer

        # model.config.temperature = 0.02
        # print(loaded_model)


class GgufRegistry(AbstractFactory):
    def register(self, model: Llama, model_name: str) -> ModelRegistryCreate:
        """
        Private Model을 Model Repository에 저장하는 method

        * Parmas
            * repo: Model 공급 유형에 따라 달라짐
                - Huggingface transfromers : repo_id
                - Huggingface gguf : repo_id, file_name
        """
        mlflow.set_experiment(self._experiment_name)
        model_name = model_name.replace("/", "-")
        with mlflow.start_run() as run:
            mlflow.pyfunc.log_model(
                artifact_path=model_name, python_model=LlamaModelWrapper(model), registered_model_name=model_name
            )
            run_info = self._get_run_info(run.info.run_id, model_name)
        return run_info
        # model_uri = f"models:/{model_name}/latest"
        # loaded_model = mlflow.pyfunc.load_model(model_uri)
        # llm = loaded_model.predict("")
        # print(llm)
        # print("Test Result!!!", llm.create_chat_completion(


# messages = [
# 	{
# 		"role": "user",
# 		"content": "What is the capital of France?"
# 	}
# ]
# ))


class LlamaModelWrapper(PythonModel):
    def __init__(self, model):
        self.model = model

    def predict(self, context, model_input):
        if self.model is None:
            raise ValueError("The model has not been loaded. " "Ensure that 'load_context' is properly executed.")
        return self.model
