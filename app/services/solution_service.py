from io import BytesIO
from pathlib import Path

from config.settings import get_settings
from fastapi import UploadFile
from langchain_core.documents import Document
from repos.solution import solution_config_repository, solution_repository
from schemas.solution import (
    SolutionBaseSchema,
    SolutionConfigBaseSchema,
    SolutionConfigReadSchema,
    SolutionReadSchema,
)
from sqlalchemy.orm import Session

settings = get_settings()


class SolutionService:
    def __init__(self):
        ...

    def create(self, db: Session, obj_in: SolutionBaseSchema):
        result = solution_repository.create(db, obj_in=obj_in)
        return result

    def get(self, db: Session, pk: int) -> SolutionReadSchema:
        return solution_repository.get(db, pk)

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> list[SolutionReadSchema]:
        return solution_repository.get_multi(db, skip=skip, limit=limit)

    def get_all(self, db: Session) -> list[SolutionReadSchema]:
        return solution_repository.get_all(db)

    def update(self, db: Session, db_obj, obj_in):
        return solution_repository.update(db, db_obj=db_obj, obj_in=obj_in)


class SolutionConfigService:
    def __init__(self):
        ...

    def create(self, db: Session, obj_in: SolutionConfigBaseSchema):
        result = solution_config_repository.create(db, obj_in=obj_in)
        return result

    def get(self, db: Session, pk: int) -> SolutionConfigReadSchema:
        return solution_config_repository.get(db, pk)

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> list[SolutionConfigReadSchema]:
        return solution_config_repository.get_multi(db, skip=skip, limit=limit)

    def get_all(self, db: Session) -> list[SolutionConfigReadSchema]:
        return solution_config_repository.get_all(db)

    def update(self, db: Session, db_obj, obj_in):
        return solution_config_repository.update(db, db_obj=db_obj, obj_in=obj_in)

