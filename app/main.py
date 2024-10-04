# from core.middlewares import log_and_handle_exceptions
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import api_router

SWAGGER_TITLE = "SURROMIND Chatbot"
SWAGGER_SUMMARY = "생성 AI 솔루션 팀 Chatbot MVP v0.1"
SWAGGER_DESCRIPTION = """
Demo Page
* [Chatbot](https://dev-surrochat-ui.surromind.ai/)
* [Backoffice](https://dev-surrochat-backoffice.surromind.ai/)

프로젝트 구성 ([개발환경 컨플루언스](https://surromind.atlassian.net/wiki/spaces/SURROMIND/pages/171311198))
1. RestfulAPI Server : FastAPI
2. Chat Model Module : Langchain
3. Storage
    1) Document DB : OpenSearch (2.14.0)
    2) Vector DB : Milvus (2.4.4)
    3) RDBMS : MariaDB (10.11)
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
