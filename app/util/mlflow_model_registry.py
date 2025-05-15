from abc import ABC, abstractmethod
from typing import Any, Optional
import mlflow
from mlflow.models import ModelSignature
from mlflow.tracking import MlflowClient
import logging


logger = logging.getLogger(__name__)

    
class MLflowConnectionManager:
    """MLflow 연결 관리를 위한 클래스"""
    
    def __init__(
        self,
        tracking_uri: str,
        experiment_name: str,
    ):
        """MLflow 연결을 초기화합니다
        
        Args:
            tracking_uri: MLflow 서버의 URI 주소
            experiment_name: 사용할 MLflow 실험 이름
        """
        self.tracking_uri = tracking_uri
        self.experiment_name = experiment_name
        self._setup_connection()
        
    def _setup_connection(self) -> None:
        """MLflow 연결을 설정합니다"""
        try:
            # Tracking URI 설정
            if self.tracking_uri:
                mlflow.set_tracking_uri(self.tracking_uri)
                logger.info(f"Set MLflow tracking URI to: {self.tracking_uri}")
            
            # Experiment 설정
            if self.experiment_name:
                experiment = mlflow.get_experiment_by_name(self.experiment_name)
                if experiment is None:
                    experiment_id = mlflow.create_experiment(self.experiment_name)
                    logger.info(f"Created new experiment: {self.experiment_name}")
                else:
                    experiment_id = experiment.experiment_id
                mlflow.set_experiment(experiment_id)
                logger.info(f"Set experiment to: {self.experiment_name}")
            
            # Client 초기화
            self.client = MlflowClient()
            
        except Exception as e:
            logger.error(f"Failed to setup MLflow connection: {str(e)}")
            raise


class ModelRegistryBase(ABC):
    """모델 레지스트리 작업을 위한 기본 추상 클래스"""
    
    def __init__(
        self,
        model_name: str,
        connection_manager: MLflowConnectionManager,
        model_version: Optional[str] = None
    ):
        self.model_name = model_name
        self.connection_manager = connection_manager
        self.model_version = model_version
        self.client = self.connection_manager.client
        
    def register_model(self, run_id: str, artifact_path: str) -> tuple[str, str]:
        """모델을 모델 레지스트리에 등록합니다
        
        Args:
            run_id: MLflow run ID
            artifact_path: 모델 아티팩트 경로
            
        Returns:
            등록된 모델의 버전
        """
        try:
            model_uri = f"runs:/{run_id}/{artifact_path}"
            try:
                self.client.get_registered_model(self.model_name)
            except Exception:
                self.client.create_registered_model(self.model_name)
                logger.info(f"Created registered model: {self.model_name}")
            model_details = self.client.create_model_version(
                name=self.model_name,
                source=model_uri,
                run_id=run_id
            )
            model_version = model_details.version
            logger.info(f"Registered model version: {model_version}")
            return model_uri, model_version
        except Exception as e:
            logger.error(f"Failed to register model: {str(e)}")
            raise
    
    def transition_model_version(
        self,
        version: str,
        stage: str,
        archive_existing_versions: bool = False
    ) -> None:
        """모델 버전의 단계를 변경합니다
        
        Args:
            version: 모델 버전
            stage: 변경할 단계 (예: 'Staging', 'Production', 'Archived')
            archive_existing_versions: 기존 버전을 보관할지 여부
        """
        try:
            self.client.transition_model_version_stage(
                name=self.model_name,
                version=version,
                stage=stage,
                archive_existing_versions=archive_existing_versions
            )
            logger.info(f"Transitioned model {self.model_name} version {version} to {stage}")
        except Exception as e:
            logger.error(f"Failed to transition model version: {str(e)}")
            raise
    
    @abstractmethod
    def log_model(self, model: Any, artifact_path: str, **kwargs: dict[str, Any]) -> str:
        """MLFlow 모델 레지스트리에 모델을 기록합니다
        
        Args:
            model: 기록할 모델
            artifact_path: 모델 아티팩트가 저장될 경로
            **kwargs: 각 플레이버에 특화된 추가 인자
            
        Returns:
            MLflow run ID
        """
        pass
    
    @abstractmethod
    def load_model(self, model_uri: str) -> Any:
        """MLFlow 모델 레지스트리에서 모델을 로드합니다
        
        Args:
            model_uri: 로드할 모델의 URI
            
        Returns:
            로드된 모델
        """
        pass


class TransformersModelRegistry(ModelRegistryBase):
    """HuggingFace Transformers 모델을 위한 구현체"""
    
    def log_model(
        self,
        model: Any,
        artifact_path: str,
        tokenizer: Optional[Any] = None,
        model_signature: Optional[ModelSignature] = None,
    ) -> str:
        """MLFlow 모델 레지스트리에 transformers 모델을 기록합니다
        
        Args:
            model: HuggingFace 모델
            artifact_path: 모델 아티팩트가 저장될 경로
            tokenizer: HuggingFace 토크나이저
            model_signature: MLFlow 모델 시그니처
            **kwargs: mlflow.transformers.log_model을 위한 추가 인자
            
        Returns:
            MLflow run ID
        """
        try:
            with mlflow.start_run() as run:
                mlflow.transformers.log_model(
                    transformers_model=model,
                    artifact_path=artifact_path,
                    tokenizer=tokenizer,
                    model_signature=model_signature,
                )
                logger.info(f"Successfully logged transformers model to {artifact_path}")
                run_id = run.info.run_id
                return run_id
        except Exception as e:
            logger.error(f"Failed to log transformers model: {str(e)}")
            raise
    
    def load_model(self, model_uri: str) -> Any:
        """MLFlow 모델 레지스트리에서 transformers 모델을 로드합니다
        
        Args:
            model_uri: 로드할 모델의 URI
            
        Returns:
            로드된 transformers 모델
        """
        try:
            return mlflow.transformers.load_model(model_uri)
        except Exception as e:
            logger.error(f"Failed to load transformers model: {str(e)}")
            raise


class PyFuncModelRegistry(ModelRegistryBase):
    """Python 함수 모델(예: BGE-M3, Llama.cpp)을 위한 구현체"""
    
    def log_model(
        self,
        model: Any,
        artifact_path: str,
        model_signature: Optional[ModelSignature] = None,
        **kwargs: dict[str, Any]
    ) -> str:
        """MLFlow 모델 레지스트리에 Python 함수 모델을 기록합니다
        
        Args:
            model: Python 모델 객체
            artifact_path: 모델 아티팩트가 저장될 경로
            model_signature: MLFlow 모델 시그니처
            **kwargs: mlflow.pyfunc.log_model을 위한 추가 인자
            
        Returns:
            MLflow run ID
        """
        try:
            with mlflow.start_run() as run:
                mlflow.pyfunc.log_model(
                    artifact_path=artifact_path,
                    python_model=model,
                )
                logger.info(f"Successfully logged pyfunc model to {artifact_path}")
                run_id = run.info.run_id
                return run_id
        except Exception as e:
            logger.error(f"Failed to log pyfunc model: {str(e)}")
            raise
    
    def load_model(self, model_uri: str) -> Any:
        """MLFlow 모델 레지스트리에서 Python 함수 모델을 로드합니다
        
        Args:
            model_uri: 로드할 모델의 URI
            
        Returns:
            로드된 Python 함수 모델
        """
        try:
            return mlflow.pyfunc.load_model(model_uri)
        except Exception as e:
            logger.error(f"Failed to load pyfunc model: {str(e)}")
            raise


class ModelRegistryFactory:
    """적절한 모델 레지스트리 인스턴스를 생성하는 팩토리 클래스"""
    
    @staticmethod
    def create_registry(
        flavor: str,
        model_name: str,
        model_version: Optional[str] = None,
        connection_manager: Optional[MLflowConnectionManager] = None
    ) -> ModelRegistryBase:
        """플레이버에 기반한 적절한 모델 레지스트리 인스턴스를 생성합니다
        
        Args:
            flavor: 모델 플레이버 유형('transformers' 또는 'pyfunc')
            model_name: 모델의 이름
            model_version: 모델의 버전
            connection_manager: MLflow 연결 관리자
            
        Returns:
            적절한 ModelRegistryBase 구현체
            
        Raises:
            ValueError: 지원되지 않는 플레이버가 제공된 경우
        """
        registry_map = {
            'transformers': TransformersModelRegistry,
            'pyfunc': PyFuncModelRegistry
        }
        
        if flavor not in registry_map:
            raise ValueError(f"Unsupported model flavor: {flavor}. Supported flavors: {list(registry_map.keys())}")
            
        return registry_map[flavor](model_name, connection_manager, model_version)

# 사용 예시:
"""
# MLflow 연결 설정
connection_manager = MLflowConnectionManager(
    tracking_uri="http://localhost:5000",
    experiment_name="my-experiment"
)

# transformers 모델의 경우
registry = ModelRegistryFactory.create_registry(
    'transformers',
    'my-model',
    connection_manager=connection_manager
)

# 모델 로깅 및 등록
run_id = registry.log_model(
    model=transformer_model,
    artifact_path='models/transformer',
    tokenizer=tokenizer
)

# 모델 버전 등록
version = registry.register_model(run_id, 'models/transformer')

# 모델 단계 변경
registry.transition_model_version(version, 'Production')

# Python 함수 모델의 경우
registry = ModelRegistryFactory.create_registry(
    'pyfunc',
    'my-model',
    connection_manager=connection_manager
)

# 모델 로깅 및 등록
run_id = registry.log_model(
    model=python_model,
    artifact_path='models/pyfunc'
)
version = registry.register_model(run_id, 'models/pyfunc')
"""
