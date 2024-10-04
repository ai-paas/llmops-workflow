from io import BytesIO
from pathlib import Path

from fastapi import UploadFile
from langchain_core.documents import Document
from repos.prompt import prompt_repository, prompt_variable_repository
from schemas.prompt import (
    PromptBaseSchema,
    PromptCreateSchema,
    PromptReadSchema,
    PromptVariableBaseSchema,
    PromptVariableReadSchema,
)
from sqlalchemy.orm import Session


class PromptService:
    def __init__(self):
        ...

    def create(self, db: Session, obj_in: PromptCreateSchema) -> PromptReadSchema:
        prompt_obj_in = obj_in.prompt
        variables = obj_in.prompt_variable
        prompt_obj = prompt_repository.create(db, obj_in=prompt_obj_in)
        prompt_id = prompt_obj.id
        if variables:
            for variable in variables:
                prompt_variable_repository.create(
                    db, obj_in=PromptVariableBaseSchema(prompt_id=prompt_id, name=variable)
                )
        result = prompt_repository.get(db, prompt_id)
        return result

    def get(self, db: Session, pk: int) -> PromptReadSchema:
        return prompt_repository.get(db, pk)

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> list[PromptReadSchema]:
        return prompt_repository.get_multi(db, skip=skip, limit=limit)

    def get_all(self, db: Session) -> list[PromptReadSchema]:
        return prompt_repository.get_all(db)

    def update(self, db: Session, db_obj, obj_in):
        prompt_obj_in = obj_in.prompt
        variables = obj_in.prompt_variable
        prompt_obj = prompt_repository.update(db, db_obj=db_obj, obj_in=prompt_obj_in)
        prompt_id = prompt_obj.id
        existing_variables = prompt_variable_repository.filter(db, {"prompt_id": prompt_id})

        if existing_variables:
            for variable in existing_variables:
                prompt_variable_repository.delete(db, pk=variable.id)

        if variables:
            for variable in variables:
                prompt_variable_repository.create(
                    db, obj_in=PromptVariableBaseSchema(prompt_id=prompt_id, name=variable)
                )
        result = prompt_repository.get(db, prompt_id)
        return result


class PromptVariableService:
    ...
