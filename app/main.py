# from core.middlewares import log_and_handle_exceptions
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import api_router

SWAGGER_TITLE = "AI-PaaS RAG Workflow"
SWAGGER_SUMMARY = "RAG Workflow Backend Server"
SWAGGER_DESCRIPTION = """
주요 기능
1. Model
    - Pre-trained, Fine-tuned, embedding, Re-rank Model을 등록하고 불러옵니다.
2. Knowledge
    - RAG(검색 증강 기술)에서 활용할 지식 데이터를 저장하고 검색에 활용 합니다.
    - 저장소 : VectorDB(Milvus)
3. Prompt
    - Prompt를 사용자가 생성하고 solution에 활용할 수 있도록 합니다.
4. Solution
    - Chat, workflow 등과 같은 Solution을 생성합니다.
"""


app = FastAPI(title=SWAGGER_TITLE, summary=SWAGGER_SUMMARY, description=SWAGGER_DESCRIPTION)
# app.middleware("http")(log_and_handle_exceptions)

# CORS 설정
origins = [
    "*",  # 모든 출처 허용
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
