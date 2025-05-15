from abc import ABC, abstractmethod
from typing import Any, Optional, Union
import numpy as np
from mlflow.pyfunc.model import PythonModel, PythonModelContext
import logging

logger = logging.getLogger(__name__)

class BaseModelWrapper(ABC, PythonModel):
    """MLflow의 PythonModel 인터페이스를 구현하는 모델 래퍼의 기본 추상 클래스"""
    
    def __init__(self, model: Any, **kwargs: dict[str, Any]):
        """래퍼를 모델 인스턴스로 초기화합니다.
        
        Args:
            model: 기본 모델 인스턴스
            **kwargs: 추가적인 모델별 매개변수
        """
        self.model = model
        self.model_kwargs: dict[str, Any] = kwargs
        
    @abstractmethod
    def predict(
        self,
        context: PythonModelContext,
        model_input: Any,
        params: Optional[dict[str, Any]] = None
    ) -> Any:
        """래핑된 모델을 사용하여 예측을 수행합니다.
        
        Args:
            context: MLflow 컨텍스트
            model_input: 예측을 위한 입력 데이터
            params: 예측을 위한 선택적 매개변수
            
        Returns:
            모델 예측 결과
        """
        pass
    
    @abstractmethod
    def load_context(self, context: PythonModelContext) -> None:
        """컨텍스트에서 모델을 로드합니다.
        
        Args:
            context: 모델 아티팩트를 포함하는 MLflow 컨텍스트
        """
        pass

class BGEM3Wrapper(BaseModelWrapper):
    """BGE-M3 임베딩 모델을 위한 래퍼"""
    
    def __init__(
        self,
        model: Any,
        batch_size: int = 12,
        max_length: int = 8192,
        normalize_embeddings: bool = True,
        **kwargs: dict[str, Any]
    ):
        """BGE-M3 래퍼를 초기화합니다.
        
        Args:
            model: BGE-M3 모델 인스턴스
            batch_size: 인코딩을 위한 배치 크기
            max_length: 최대 시퀀스 길이
            normalize_embeddings: 임베딩 정규화 여부
            **kwargs: 추가 모델 매개변수
        """
        super().__init__(model, **kwargs)
        self.batch_size = batch_size
        self.max_length = max_length
        self.normalize_embeddings = normalize_embeddings
        
    def predict(
        self,
        context: PythonModelContext,
        model_input: Union[str, list[str]],
        params: Optional[dict[str, Any]] = None
    ) -> Union[np.ndarray, dict[str, Any]]:
        """입력 텍스트에 대한 임베딩을 생성합니다.
        
        Args:
            context: MLflow 컨텍스트
            model_input: 입력 텍스트, 텍스트 리스트
            params: 예측을 위한 선택적 매개변수
            
        Returns:
            numpy 배열 형태의 임베딩 또는 임베딩과 메타데이터가 포함된 딕셔너리
        """
        try:
            # 다양한 입력 유형 처리
            if isinstance(model_input, str):
                sentences = [model_input]
            elif isinstance(model_input, list):
                sentences = model_input
            else:
                raise ValueError("입력은 문자열, 문자열 리스트여야 합니다")
            
            # 임베딩 생성
            embeddings = self.model.encode(
                sentences,
                batch_size=self.batch_size,
                max_length=self.max_length,
                normalize_embeddings=self.normalize_embeddings
            )
            
            return embeddings
            
        except Exception as e:
            logger.error(f"임베딩 생성 중 오류 발생: {str(e)}")
            raise
    
    def load_context(self, context: PythonModelContext) -> None:
        """컨텍스트에서 모델을 로드합니다.
        
        Args:
            context: 모델 아티팩트를 포함하는 MLflow 컨텍스트
        """
        try:
            # 모델은 이미 __init__에서 로드되었지만, 필요한 경우 추가 아티팩트를 로드할 수 있습니다
            if context.artifacts:
                # 여기에서 추가 아티팩트 로드
                pass
        except Exception as e:
            logger.error(f"모델 컨텍스트 로드 중 오류 발생: {str(e)}")
            raise

# 사용 예시:
"""
from FlagEmbedding import BGEM3FlagModel
from app.util.model_wrappers import BGEM3Wrapper
from app.util.mlflow_model_registry import ModelRegistryFactory

# 모델 생성 및 래핑
model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
wrapped_model = BGEM3Wrapper(
    model=model,
    batch_size=12,
    max_length=8192,
    normalize_embeddings=True
)

# MLflow에 로깅
registry = ModelRegistryFactory.create_registry('pyfunc', 'bge-m3-model')
registry.log_model(
    model=wrapped_model,
    artifact_path='models/bge-m3',
    conda_env={
        'channels': ['conda-forge'],
        'dependencies': [
            'python=3.8',
            'pip',
            {
                'pip': [
                    'mlflow',
                    'torch',
                    'transformers',
                    'FlagEmbedding'
                ]
            }
        ]
    }
)

# 모델 로드 및 사용
loaded_model = registry.load_model('models/bge-m3')
embeddings = loaded_model.predict(['BGE M3란 무엇인가요?', 'BM25의 정의'])
""" 