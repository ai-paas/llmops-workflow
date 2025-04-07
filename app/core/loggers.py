import logging
from pathlib import Path

LOGGER_NAME = "aipaas-llmops"


class LoggerHandler:
    _instance = None
    initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._initialize()
        return cls._instance

    @classmethod
    def _initialize(cls):
        if not cls.initialized:
            cls.logs_directory = Path("./logs")
            cls.logs_directory.mkdir(parents=True, exist_ok=True)
            cls.log_level = logging.DEBUG
            cls.initialized = True  # 이제 클래스가 초기화되었다고 표시

    @staticmethod
    def stream_handler():
        if not LoggerHandler.initialized:
            LoggerHandler._initialize()  # 핸들러 요청 시 클래스가 초기화되었는지 확인

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(levelname)s] - %(asctime)s - %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setLevel(LoggerHandler.log_level)
        handler.setFormatter(formatter)
        return handler


def set_logger():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(LoggerHandler.log_level if LoggerHandler.initialized else logging.INFO)
    logger.addHandler(LoggerHandler.stream_handler())


set_logger()  # 로거 설정


def get_logger(logger_name: str=LOGGER_NAME):
    return logging.getLogger(logger_name)
