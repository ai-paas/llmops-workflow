# RAG-Workflow

RAG-Workflow는 지식 데이터를 벡터화하여 효과적으로 관리하고, 등록된 지식을 기반으로 사용자의 질의에 적합한 답변을 생성할 수 있도록 설계된 시스템입니다. 사용자는 이 시스템을 통해 대규모의 비정형 데이터를 처리하고, 그에 맞는 적절한 응답을 받을 수 있습니다.

## Tech Stack

![Python Icon](https://img.shields.io/badge/python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI Icon](https://img.shields.io/badge/fastapi-009688?style=flat&logo=fastapi&logoColor=white)  
![HuggingFace Icon](https://img.shields.io/badge/huggingface-fcbf29?style=flat&logo=huggingface&logoColor=white)
![llamacpp Icon](https://img.shields.io/badge/llamacpp-430098?style=flat)   
![MLFlow Icon](https://img.shields.io/badge/mlflow-0194E2?style=flat&logo=mlflow&logoColor=white)
![MariaDB Icon](https://img.shields.io/badge/mariadb-003545?style=flat&logo=mariadb&logoColor=white)



# Demo

![Demo Screenshot](./screenshot.png)

RAG-Workflow의 실제 동작 예시는 위의 스크린샷을 참고해주세요.

# Key Features

RAG(Retriever-Augmented Generation) 기반 워크플로우의 주요 기능은 다음과 같습니다:

1. **지식 기반 질의응답**: RAG-Workflow는 사전 학습된 자연어 처리 모델과 벡터화를 통해 대규모의 지식 베이스에서 관련 정보를 빠르게 검색하여 질의에 맞는 적절한 답변을 생성합니다.
   
2. **지식 데이터 벡터화**: 문서나 텍스트 데이터를 벡터화하여 데이터베이스에 저장하며, 이를 통해 효율적으로 유사한 정보를 검색할 수 있습니다.
   
3. **모듈화된 시스템**: Python, FastAPI, 그리고 HuggingFace를 활용한 모듈화된 구조로 쉽게 확장 가능하며, 필요에 따라 모델을 교체하거나 성능을 튜닝할 수 있습니다.

4. **사용자 맞춤형 질의응답 제공**: 등록된 지식 데이터를 기반으로 사용자가 제시한 질의에 맞춤형 답변을 생성할 수 있습니다.

5. **효율적인 모델 관리**: MLFlow를 통해 모델 버전 관리 및 학습 기록을 체계적으로 관리하며, 데이터베이스로는 MariaDB를 사용하여 벡터화된 데이터를 관리합니다.

# System Architecture

RAG-Workflow의 시스템 아키텍처는 아래와 같습니다:

![System Architecture](./architecture.png)

1. **데이터 수집 및 벡터화**: 텍스트 데이터는 HuggingFace 모델을 사용해 벡터화되고 MariaDB에 저장됩니다.
2. **질의 처리**: 사용자가 질의를 제출하면 FastAPI를 통해 요청이 접수되며, 벡터화된 지식 베이스를 탐색해 관련된 정보를 추출합니다.
3. **응답 생성**: 추출된 정보를 기반으로 RAG 모델을 사용해 최종 응답을 생성합니다.
4. **모델 및 데이터 관리**: MLFlow를 통해 학습된 모델을 관리하고, 필요시 모델 업데이트 또는 새로운 데이터 추가가 가능합니다.

# DB Migration

```shell
alembic revision --autogenerate -m "Your message"
alembic head
```

# Get Started

# License


