from abc import ABC, abstractclassmethod


class BaseModel(ABC):
    @abstractclassmethod
    def register_to_mlflow(self, model_name: str, *, file_name: str = None):
        ...
