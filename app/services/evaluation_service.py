from repos.knowledge import knowledge_repository
from schemas.evaluation import RetrievalRequestSchema, RetrievalResponseSchema
from sqlalchemy.orm import Session
from util.chunk import file_load_and_split, get_file_extension
from util.embedding import BGEM3Embedding
from util.vector_database import MilvusSearchManager


class EvaluationService:
    @staticmethod
    def retrieve(request: RetrievalRequestSchema, db: Session):
        knowledge_model = knowledge_repository.get(db, request.knowledge_id)
        collection_name = knowledge_model.name
        query = request.query
        top_k = request.top_k
        threshold_score = request.threshold_score
        search_type_id = request.search_type_id

        embeddings = BGEM3Embedding([query])
        dense_vector = embeddings.dense_vector
        sparse_vector = embeddings.sparse_vector

        search_manager = MilvusSearchManager(collection_name, top_k)

        # TODO: 기준 정보 별도 관리 필요
        if search_type_id == 1:  # Semantic Search
            search_result = search_manager.dense_search(dense_vector)
        elif search_type_id == 2:  # Full-Text Search
            search_result = search_manager.sparse_search(sparse_vector)
        elif search_type_id == 3:  # Hybrid Search
            dense_weight = request.dense_weight
            sparse_weight = request.sparse_weight
            search_result = search_manager.hybrid_search(dense_vector, sparse_vector, dense_weight, sparse_weight)
        else:
            result = []
        result = [
            {"distance": data.distance, "text": data.get("text")}
            for data in search_result[0]
            if data.distance > threshold_score
        ]
        return result
