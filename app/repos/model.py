from db.models import Model, ModelFormat, ModelRegistry
from repos.base import CRUDBase
from schemas.model import ModelBaseSchema, ModelFormatBaseSchema, ModelRegistryBaseSchema


class ModelRepository(CRUDBase[Model, ModelBaseSchema, ModelBaseSchema]):
    ...


class ModelRegistryRepository(CRUDBase[ModelRegistry, ModelRegistryBaseSchema, ModelRegistryBaseSchema]):
    ...
    

class ModelFormatRepository(CRUDBase[ModelFormat, ModelFormatBaseSchema, ModelFormatBaseSchema]):
    ...

model_repository = ModelRepository(Model)
model_registry_repository = ModelRegistryRepository(ModelRegistry)
model_format_repository = ModelFormatRepository(ModelFormat)