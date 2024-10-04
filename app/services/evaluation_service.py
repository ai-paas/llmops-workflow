from repos.knowledge import knowledge_repository
from schemas.evaluation import RetrievalRequestSchema, RetrievalResponseSchema
from sqlalchemy.orm import Session
from util.chunk import file_load_and_split, get_file_extension
from util.embedding import BGEM3Embedding
from util.vector_database import MilvusManager


class EvaluationService:
    def retrieve(self, request: RetrievalRequestSchema, db: Session):
        knowledge_model = knowledge_repository.get(db, request.knowledge_id)
        collection_name = knowledge_model.name
        query = request.query
        top_k = request.top_k
        threshold_score = request.threshold_score

        embeddings = BGEM3Embedding([query])
        dense_vector = embeddings.dense_vector
        sparse_vector = embeddings.sparse_vector

        search_result = MilvusManager.consine_search(dense_vector, collection_name, top_k)
        result = [
            {"distance": data.get("distance"), "text": data.get("entity").get("text")}
            for data in search_result[0]
            if data.get("distance") > threshold_score
        ]
        return result
