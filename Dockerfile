FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04 as builder

WORKDIR /app

# 타임존 설정
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    locales \
    git \
    wget \
    net-tools \
    vim \
    openssh-server \
    awscli \
    python3-pip \
    nano \
    curl \
    gcc \
    build-essential \
    sudo \
    && pip3 install pipenv

# 한글 설정
RUN localedef -f UTF-8 -i ko_KR ko_KR.UTF-8

# Copy only the Pipfile and Pipfile.lock to leverage Docker cache
COPY Pipfile Pipfile.lock ./

# Install the dependencies via pipenv
RUN pipenv install --deploy --system
FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04

WORKDIR /app

# 타임존 설정
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    libreoffice \
    python3-pip
RUN pip install six==1.16.0

# Copy the dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the FastAPI app code into the container
COPY . .
EXPOSE 8000

CMD ["fastapi", "run", "app/main.py"]
