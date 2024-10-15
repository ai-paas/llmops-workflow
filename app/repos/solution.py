from db.models import Solution, SolutionConfig
from repos.base import CRUDBase
from schemas.solution import SolutionBaseSchema, SolutionConfigBaseSchema
from sqlalchemy.orm import Session


class SolutionRepository(CRUDBase[Solution, SolutionBaseSchema, SolutionBaseSchema]):
    ...


class SolutionConfigRepository(CRUDBase[SolutionConfig, SolutionConfigBaseSchema, SolutionConfigBaseSchema]):
    ...


solution_repository = SolutionRepository(Solution)
solution_config_repository = SolutionConfigRepository(SolutionConfig)
