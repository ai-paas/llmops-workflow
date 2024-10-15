from io import BytesIO
from pathlib import Path

from fastapi import UploadFile
from langchain_core.documents import Document
from repos.knowledge import knowledge_file_repository, knowledge_repository
from schemas.knowledge import (
    KnowledgeBaseSchema,
    KnowledgeFileBaseSchema,
    KnowledgeReadSchema,
)
from sqlalchemy.orm import Session
from util.chunk import file_load_and_split, get_file_extension
from util.embedding import BGEM3Embedding
from util.object_storage import FileManager
from util.vector_database import MilvusManager


class KnowledgeService:
    def __init__(self):
        ...

    def create(self, db: Session, obj_in: KnowledgeBaseSchema):
        collection_name = obj_in.name
        MilvusManager.create_collection(collection_name)
        result = knowledge_repository.create(db, obj_in=obj_in)
        return result

    def get(self, db: Session, pk: int) -> KnowledgeReadSchema:
        return knowledge_repository.get(db, pk)

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> list[KnowledgeReadSchema]:
        return knowledge_repository.get_multi(db, skip=skip, limit=limit)

    def get_all(self, db: Session) -> list[KnowledgeReadSchema]:
        return knowledge_repository.get_all(db)

    def update(self, db: Session, db_obj, obj_in):
        return knowledge_repository.update(db, db_obj=db_obj, obj_in=obj_in)


class KnowledgeDatasetService:
    def create_dataset(self, knowledge_id: int, file: UploadFile, db: Session):
        # 1. knowledge 정보 불러오기
        knowledge_model = knowledge_repository.get(db, knowledge_id)
        collection_name = knowledge_model.name
        try:
            # 2. Storage 저장
            file_data, filename, ext, filepath = self.save_to_storage(file, collection_name)
            # 3. Chunking
            chunk_length = knowledge_model.chunk_length
            overlap = knowledge_model.overlap
            file_chunks = file_load_and_split(file_data, filename, chunk_length, overlap)
            # DB Insert
            obj_in = KnowledgeFileBaseSchema(
                name=filename, path=filepath, knowledge_id=knowledge_id, file_type=ext, chunk_number=len(file_chunks)
            )
            result = knowledge_file_repository.create(db, obj_in=obj_in)

            # # 4. Embedding into Vector Database
            partition_name = f"{collection_name}_{result.id}"
            self.embed_to_milvus(file_chunks, collection_name, partition_name)
        except Exception:
            # TODO Logging으로 변경
            print("Error!")
            return []
        db.commit()

        return result

    @staticmethod
    def get_file_object(bucket_name: str, filename: str) -> BytesIO:
        file_obj = FileManager.get_object(bucket_name, filename)
        file_stream = file_obj["Body"].read()
        return BytesIO(file_stream)

    @staticmethod
    def embed_to_milvus(chunks: list[Document], collection_name: str, partition_name: str):
        texts = [chunk.page_content for chunk in chunks]

        embeddings = BGEM3Embedding(texts)
        dense_vector = embeddings.dense_vector
        sparse_vector = embeddings.sparse_vector

        entities = [
            {"sparse_vector": entity[0], "dense_vector": entity[1], "text": entity[2]}
            for entity in zip(sparse_vector, dense_vector, texts)
        ]

        # # TODO: Collection name 하드코딩 제거
        MilvusManager.embed_documents(collection_name, entities, partition_name)

    @staticmethod
    def save_to_storage(file: UploadFile, collection_name: str):
        # TODO: 하드코딩 제거
        bucket_name = "ai-paas"
        file_name = file.filename
        file_path = f"{collection_name}/{file_name}"
        ext = get_file_extension(file)
        file_data = file.file.read()
        byteio_file_data = BytesIO(file_data)

        FileManager.upload(byteio_file_data, bucket_name, file_path)
        return file_data, file_name, ext, file_path
