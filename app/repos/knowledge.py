from db.models import Knowledge, KnowledgeFile
from repos.base import CRUDBase
from schemas.knowledge import KnowledgeBaseSchema, KnowledgeFileBaseSchema
from sqlalchemy.orm import Session


class KnowledgeRepository(CRUDBase[Knowledge, KnowledgeBaseSchema, KnowledgeBaseSchema]):
    ...


class KnowledgeFileRepository(CRUDBase[KnowledgeFile, KnowledgeFileBaseSchema, KnowledgeFileBaseSchema]):
    ...


knowledge_repository = KnowledgeRepository(Knowledge)
knowledge_file_repository = KnowledgeFileRepository(KnowledgeFile)
