from pydantic import BaseModel, Field
from typing import List, Optional, Generic, TypeVar, Dict
from datetime import datetime

T = TypeVar('T')

class ResponseFormatSchema(BaseModel, Generic[T]):
    status: int = Field(..., description="HTTP 상태 코드")
    message: str = Field(..., description="응답 메시지")
    pagination: Optional[dict[str, int]] = Field(None, description="페이지네이션 정보")
    data: Optional[T] = Field(None, description="응답 데이터")

class MLflowInfoResponse(BaseModel):
    run_id: str = Field(..., description="MLflow Run ID")
    experiment_id: str = Field(..., description="MLflow Experiment ID")
    artifact_uri: str = Field(..., description="MLflow Artifact URI")
    model_uri: str = Field(..., description="MLflow Model URI")

class ModelResponse(BaseModel):
    id: str = Field(..., description="모델 고유 ID")
    name: str = Field(..., description="사용자 입력 모델 이름")
    description: str = Field(..., description="모델에 대한 설명")
    task: str = Field(..., description="모델이 하는 일")
    type: str = Field(..., description="모델 종류")
    format: str = Field(..., description="모델 포맷")
    version: str = Field(..., description="모델 버전")
    model_id: str = Field(..., description="모델 ID")
    params: float = Field(..., description="모델 파라미터")
    file_path: Optional[str] = Field(None, description="업로드된 모델 파일 경로")
    mlflow_info: MLflowInfoResponse = Field(..., description="MLflow 정보")
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="수정 시간")

class ModelListResponse(BaseModel):
    total: int = Field(..., description="전체 모델 수")
    models: List[ModelResponse] = Field(..., description="모델 목록")

class BasicInfoResponse(BaseModel):
    name: str = Field(..., description="데이터셋 이름")
    description: str = Field(..., description="데이터셋 설명")
    language: str = Field(..., description="데이터셋 언어")

class ChunkSettingsResponse(BaseModel):
    chunk_size: int = Field(..., description="청크 길이")
    chunk_overlap: int = Field(..., description="청크 중첩 크기")
    chunk_type: str = Field(..., description="청크 타입")

class EmbeddingSettingsResponse(BaseModel):
    embedding_model: str = Field(..., description="임베딩 모델 ID")

class SearchSettingsResponse(BaseModel):
    search_method: str = Field(..., description="검색 방법")
    top_k: int = Field(..., description="검색 결과 개수")
    threshold: float = Field(..., description="검색 임계값")

class DatasetResponse(BaseModel):
    id: str = Field(..., description="데이터셋 고유 ID")
    basic_info: BasicInfoResponse = Field(..., description="기본 정보")
    chunk_settings: ChunkSettingsResponse = Field(..., description="청크 설정")
    embedding_settings: EmbeddingSettingsResponse = Field(..., description="임베딩 설정")
    search_settings: SearchSettingsResponse = Field(..., description="검색 설정")
    file_path: Optional[str] = Field(None, description="업로드된 파일 경로")
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="수정 시간")

class DatasetListResponse(BaseModel):
    total: int = Field(..., description="전체 데이터셋 수")
    datasets: List[DatasetResponse] = Field(..., description="데이터셋 목록")

class DatasetFileResponse(BaseModel):
    id: str = Field(..., description="파일 고유 ID")
    dataset_id: str = Field(..., description="데이터셋 ID")
    filename: str = Field(..., description="파일 이름")
    file_path: str = Field(..., description="파일 경로")
    description: Optional[str] = Field(None, description="파일 설명")
    created_at: datetime = Field(..., description="생성 시간")

class DatasetFileListResponse(BaseModel):
    total: int = Field(..., description="전체 파일 수")
    files: List[DatasetFileResponse] = Field(..., description="파일 목록")

class PromptVariableResponse(BaseModel):
    name: str = Field(..., description="변수 이름")
    description: str = Field(..., description="변수 설명")
    type: str = Field(..., description="변수 타입")
    required: bool = Field(..., description="필수 여부")
    default_value: Optional[str] = Field(None, description="기본값")

class PromptResponse(BaseModel):
    id: str = Field(..., description="프롬프트 고유 ID")
    name: str = Field(..., description="프롬프트 이름")
    description: str = Field(..., description="프롬프트 설명")
    content: str = Field(..., description="프롬프트 내용")
    variables: List[PromptVariableResponse] = Field(..., description="프롬프트 변수 목록")
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="수정 시간")

class PromptListResponse(BaseModel):
    total: int = Field(..., description="전체 프롬프트 수")
    prompts: List[PromptResponse] = Field(..., description="프롬프트 목록")

class ServingStatusResponse(BaseModel):
    status: str = Field(..., description="서빙 상태 (running, pending, failed, stopped)")
    ready_replicas: int = Field(..., description="준비된 파드 수")
    total_replicas: int = Field(..., description="전체 파드 수")
    last_error: Optional[str] = Field(None, description="마지막 에러 메시지")
    last_updated: datetime = Field(..., description="마지막 상태 업데이트 시간")

class ServingEndpointResponse(BaseModel):
    url: str = Field(..., description="서빙 엔드포인트 URL")
    port: int = Field(..., description="서빙 포트")
    protocol: str = Field(..., description="프로토콜 (http, grpc)")

class ModelServingResponse(BaseModel):
    id: str = Field(..., description="서빙 고유 ID")
    model_id: str = Field(..., description="서빙 중인 모델 ID")
    platform: str = Field(..., description="서빙 플랫폼")
    status: ServingStatusResponse = Field(..., description="서빙 상태")
    endpoint: ServingEndpointResponse = Field(..., description="서빙 엔드포인트")
    resources: Dict[str, str] = Field(..., description="리소스 요청")
    replicas: int = Field(..., description="파드 복제 수")
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="수정 시간")

class ModelServingListResponse(BaseModel):
    total: int = Field(..., description="전체 서빙 수")
    servings: List[ModelServingResponse] = Field(..., description="서빙 목록")

class WorkflowNodeResponse(BaseModel):
    node_type: str = Field(..., description="노드 타입")
    node_id: str = Field(..., description="노드 ID")
    config: Dict[str, str] = Field(..., description="노드 설정")
    next_nodes: List[str] = Field(..., description="다음 노드 ID 목록")
    llm_config: Optional[Dict[str, float | int]] = Field(None, description="LLM 노드의 모델 설정")
    retriever_config: Optional[Dict[str, str | int | float]] = Field(None, description="Retriever 노드의 설정")

class WorkflowStatusResponse(BaseModel):
    status: str = Field(..., description="워크플로우 상태 (running, pending, failed, stopped)")
    ready_replicas: int = Field(..., description="준비된 파드 수")
    total_replicas: int = Field(..., description="전체 파드 수")
    last_error: Optional[str] = Field(None, description="마지막 에러 메시지")
    last_updated: datetime = Field(..., description="마지막 상태 업데이트 시간")

class WorkflowEndpointResponse(BaseModel):
    url: str = Field(..., description="워크플로우 엔드포인트 URL")
    port: int = Field(..., description="워크플로우 포트")
    protocol: str = Field(..., description="프로토콜 (http, grpc)")

class WorkflowResponse(BaseModel):
    id: str = Field(..., description="워크플로우 고유 ID")
    name: str = Field(..., description="워크플로우 이름")
    description: str = Field(..., description="워크플로우 설명")
    nodes: List[WorkflowNodeResponse] = Field(..., description="워크플로우 노드 목록")
    entry_node: str = Field(..., description="시작 노드 ID")
    status: WorkflowStatusResponse = Field(..., description="워크플로우 상태")
    endpoint: WorkflowEndpointResponse = Field(..., description="워크플로우 엔드포인트")
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="수정 시간")

class WorkflowListResponse(BaseModel):
    total: int = Field(..., description="전체 워크플로우 수")
    workflows: List[WorkflowResponse] = Field(..., description="워크플로우 목록")

class WorkflowMetricsResponse(BaseModel):
    total_messages: int = Field(..., description="총 메시지 수")
    active_users: int = Field(..., description="활성 사용자 수")
    last_updated: datetime = Field(..., description="마지막 업데이트 시간")

class WorkflowNodeMetricsResponse(BaseModel):
    node_id: str = Field(..., description="노드 ID")
    node_type: str = Field(..., description="노드 타입")
    total_calls: int = Field(..., description="총 호출 수")
    avg_response_time: float = Field(..., description="평균 응답 시간 (ms)")
    error_count: int = Field(..., description="에러 발생 수")
    last_updated: datetime = Field(..., description="마지막 업데이트 시간")

class WorkflowMonitoringResponse(BaseModel):
    workflow_id: str = Field(..., description="워크플로우 ID")
    metrics: WorkflowMetricsResponse = Field(..., description="워크플로우 전체 메트릭")
    node_metrics: List[WorkflowNodeMetricsResponse] = Field(..., description="노드별 메트릭")
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="수정 시간")

class OverallWorkflowMetricsResponse(BaseModel):
    total_workflows: int = Field(..., description="전체 워크플로우 수")
    total_messages: int = Field(..., description="전체 메시지 수")
    total_active_users: int = Field(..., description="전체 활성 사용자 수")
    last_updated: datetime = Field(..., description="마지막 업데이트 시간")

class WorkflowMonitoringListResponse(BaseModel):
    total: int = Field(..., description="전체 워크플로우 수")
    overall_metrics: OverallWorkflowMetricsResponse = Field(..., description="전체 워크플로우 메트릭")
    workflows: List[WorkflowMonitoringResponse] = Field(..., description="워크플로우별 모니터링 정보")