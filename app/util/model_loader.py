from FlagEmbedding import BGEM3FlagModel
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
from transformers import pipeline


class HuggingFaceModelLoader:
    @staticmethod
    def load_transformers(model_id: str, *, task: str = "text-generation"):
        """Transformers 모델을 로드합니다.
        
        Args:
            model_id: 모델 ID 또는 경로
            task: 수행할 작업 유형 (기본값: "text-generation")
            
        Returns:
            로드된 Transformers 파이프라인 객체
        """
        return pipeline(task, model=model_id)
    
    @staticmethod
    def load_sentence_transformers(model_id: str):
        """Sentence Transformers 모델을 로드합니다.
        
        Args:
            model_id: 모델 ID 또는 경로
            
        Returns:
            로드된 SentenceTransformer 모델 객체
        """
        return SentenceTransformer(model_id)
    
    @staticmethod
    def load_gguf(model_id: str, file_name: str):
        """GGUF 형식의 모델을 로드합니다.
        
        Args:
            model_id: 모델 저장소 ID
            file_name: 모델 파일 이름
            
        Returns:
            로드된 Llama 모델 객체
        """
        return Llama.from_pretrained(repo_id=model_id, filename=file_name, verbose=False)
    
    @staticmethod
    def load_bge_m3(model_id: str):
        """BGE-M3 모델을 로드합니다.
        
        Args:
            model_id: 모델 ID 또는 경로
            
        Returns:
            로드된 BGEM3FlagModel 객체
        """
        return BGEM3FlagModel(model_id, use_fp16=False)