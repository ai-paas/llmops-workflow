from db.models import Model, ModelRegistry
from repos.base import CRUDBase
from schemas.model import ModelBaseSchema, ModelRegistryBaseSchema
from sqlalchemy.orm import Session


class ModelRepository(CRUDBase[Model, ModelBaseSchema, ModelBaseSchema]):
    ...


class ModelRegistryRepository(CRUDBase[ModelRegistry, ModelRegistryBaseSchema, ModelRegistryBaseSchema]):
    ...


model_repository = ModelRepository(Model)
model_registry_repository = ModelRegistryRepository(ModelRegistry)
