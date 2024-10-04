from db.models import Prompt, PromptVariable
from repos.base import CRUDBase
from schemas.prompt import PromptBaseSchema, PromptVariableBaseSchema
from sqlalchemy.orm import Session


class PromptRepository(CRUDBase[Prompt, PromptBaseSchema, PromptBaseSchema]):
    ...


class PromptVariableRepository(CRUDBase[Prompt, PromptVariableBaseSchema, PromptVariableBaseSchema]):
    ...


prompt_repository = PromptRepository(Prompt)
prompt_variable_repository = PromptVariableRepository(PromptVariable)
