from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum


class ModelCreateSchema(BaseModel):
    name: str = Field(..., description="사용자 입력 모델 이름 (e.g.HuggingFace 모델 이름)")
    description: str = Field(..., description="모델에 대한 설명")
    model_provider_id: int = Field(..., description="모델 제공자 ID (1: HuggingFace, 2: Ollama, 3: Custom)")
    model_type_id: int = Field(..., description="모델 타입 ID (1: LLM, 2: Embedding, 3: Re-Rank, 4: Fine-Tuned)")
    model_format_id: int = Field(..., description="모델 포맷 ID (1: Transformers, 2: Sentence-Transformers, 3: GGUF, 4: BGE-M3)")


class ModelUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, description="사용자 입력 모델 이름")
    description: Optional[str] = Field(None, description="모델에 대한 설명")
    task: Optional[str] = Field(None, description="모델이 하는 일 e.g. 'Text Generation'")
    type: Optional[str] = Field(None, description="모델 종류 e.g. 'LLM, Embedding, Re-Rank'")
    format: Optional[str] = Field(None, description="모델 포맷 e.g. 'gguf, transformers, ...'")
    version: Optional[str] = Field(None, description="모델 버전 e.g. '1.0.0'")
    model_id: Optional[str] = Field(None, description="Qwen/QwQ-23B-Preview")
    params: Optional[float] = Field(None, description="모델 파라미터 e.g. 32B")


class ChunkType(str, Enum):
    TEXT = "text"
    CODE = "code"
    TABLE = "table"


class SearchMethod(str, Enum):
    VECTOR = "vector"
    KEYWORD = "keyword"
    HYBRID = "hybrid"


class BasicInfoSchema(BaseModel):
    name: str = Field(..., description="데이터셋 이름")
    description: str = Field(..., description="데이터셋 설명")
    language: str = Field(..., description="데이터셋 언어")


class ChunkSettingsSchema(BaseModel):
    chunk_size: int = Field(..., description="청크 길이")
    chunk_overlap: int = Field(..., description="청크 중첩 크기")
    chunk_type: ChunkType = Field(..., description="청크 타입 (text, code, table)")


class EmbeddingSettingsSchema(BaseModel):
    embedding_model: str = Field(..., description="임베딩 모델 ID")


class SearchSettingsSchema(BaseModel):
    search_method: SearchMethod = Field(..., description="검색 방법 (vector, keyword, hybrid)")
    top_k: int = Field(..., description="검색 결과 개수")
    threshold: float = Field(..., description="검색 임계값")


class DatasetCreateSchema(BaseModel):
    basic_info: BasicInfoSchema = Field(..., description="기본 정보")
    chunk_settings: ChunkSettingsSchema = Field(..., description="청크 설정")
    embedding_settings: EmbeddingSettingsSchema = Field(..., description="임베딩 설정")
    search_settings: SearchSettingsSchema = Field(..., description="검색 설정")


class DatasetUpdateSchema(BaseModel):
    basic_info: Optional[BasicInfoSchema] = Field(None, description="기본 정보")
    chunk_settings: Optional[ChunkSettingsSchema] = Field(None, description="청크 설정")
    embedding_settings: Optional[EmbeddingSettingsSchema] = Field(None, description="임베딩 설정")
    search_settings: Optional[SearchSettingsSchema] = Field(None, description="검색 설정")


class DatasetFileAddSchema(BaseModel):
    description: Optional[str] = Field(None, description="추가된 파일에 대한 설명")


class PromptVariableSchema(BaseModel):
    name: str = Field(..., description="변수 이름")
    description: str = Field(..., description="변수 설명")
    type: str = Field(..., description="변수 타입 (string, number, boolean, etc.)")
    required: bool = Field(..., description="필수 여부")
    default_value: Optional[str] = Field(None, description="기본값")


class PromptCreateSchema(BaseModel):
    name: str = Field(..., description="프롬프트 이름")
    description: str = Field(..., description="프롬프트 설명")
    content: str = Field(..., description="프롬프트 내용 (변수 포함)")
    variables: List[PromptVariableSchema] = Field(..., description="프롬프트 변수 목록")


class PromptUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, description="프롬프트 이름")
    description: Optional[str] = Field(None, description="프롬프트 설명")
    content: Optional[str] = Field(None, description="프롬프트 내용 (변수 포함)")
    variables: Optional[List[PromptVariableSchema]] = Field(None, description="프롬프트 변수 목록")


class ServingPlatform(str, Enum):
    OLLAMA = "ollama"
    VLLM = "vllm"
    KSERVE = "kserve"


class ResourceRequestSchema(BaseModel):
    cpu: str = Field(..., description="CPU 요청 (e.g. '1', '500m')")
    memory: str = Field(..., description="메모리 요청 (e.g. '1Gi', '512Mi')")
    gpu: Optional[str] = Field(None, description="GPU 요청 (e.g. '1', '2')")


class ServingConfigSchema(BaseModel):
    platform: ServingPlatform = Field(..., description="서빙 플랫폼 (ollama, vllm, kserve)")
    resources: ResourceRequestSchema = Field(..., description="리소스 요청")
    replicas: int = Field(1, description="파드 복제 수")
    port: int = Field(..., description="서빙 포트")
    env_vars: Optional[Dict[str, str]] = Field(None, description="환경 변수")
    platform_specific_config: Optional[Dict[str, str]] = Field(None, description="플랫폼별 특정 설정")


class ModelServingCreateSchema(BaseModel):
    model_id: str = Field(..., description="서빙할 모델 ID")
    serving_config: ServingConfigSchema = Field(..., description="서빙 설정")


class ModelServingUpdateSchema(BaseModel):
    replicas: Optional[int] = Field(None, description="파드 복제 수")
    resources: Optional[ResourceRequestSchema] = Field(None, description="리소스 요청")
    env_vars: Optional[Dict[str, str]] = Field(None, description="환경 변수")
    platform_specific_config: Optional[Dict[str, str]] = Field(None, description="플랫폼별 특정 설정")


class WorkflowNodeType(str, Enum):
    USER_QUERY = "user_query"
    LLM = "llm"
    RETRIEVER = "retriever"
    TOOL = "tool"
    PROMPT = "prompt"


class ModelConfigSchema(BaseModel):
    temperature: float = Field(0.7, description="생성 다양성 조절 (0.0 ~ 1.0)")
    top_p: float = Field(1.0, description="누적 확률 임계값 (0.0 ~ 1.0)")
    presence_penalty: float = Field(0.0, description="주제 반복 패널티 (-2.0 ~ 2.0)")
    frequency_penalty: float = Field(0.0, description="단어 반복 패널티 (-2.0 ~ 2.0)")
    max_tokens: int = Field(2048, description="최대 생성 토큰 수")


class RetrieverConfigSchema(BaseModel):
    dataset_id: str = Field(..., description="사용할 데이터셋 ID")
    search_method: str = Field(..., description="검색 방법 (vector, keyword, hybrid)")
    top_k: int = Field(..., description="검색 결과 개수")
    threshold: float = Field(..., description="검색 임계값")


class WorkflowNodeConfigSchema(BaseModel):
    node_type: WorkflowNodeType = Field(..., description="노드 타입")
    node_id: str = Field(..., description="노드 ID")
    config: Dict[str, str] = Field(..., description="노드 설정")
    next_nodes: List[str] = Field(..., description="다음 노드 ID 목록")
    llm_config: Optional[ModelConfigSchema] = Field(None, description="LLM 노드의 모델 설정")
    retriever_config: Optional[RetrieverConfigSchema] = Field(None, description="Retriever 노드의 설정")


class WorkflowCreateSchema(BaseModel):
    name: str = Field(..., description="워크플로우 이름")
    description: str = Field(..., description="워크플로우 설명")
    nodes: List[WorkflowNodeConfigSchema] = Field(..., description="워크플로우 노드 목록")
    entry_node: str = Field(..., description="시작 노드 ID")


class WorkflowUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, description="워크플로우 이름")
    description: Optional[str] = Field(None, description="워크플로우 설명")
    nodes: Optional[List[WorkflowNodeConfigSchema]] = Field(None, description="워크플로우 노드 목록")
    entry_node: Optional[str] = Field(None, description="시작 노드 ID")