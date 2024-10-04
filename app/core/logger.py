import json
import logging
from datetime import datetime
from pathlib import Path

from config.opensearch.connect import Client
from config.settings import get_settings, root_directory
from fastapi import UploadFile
from surrochat_model.utils.text_util import extract_urls


class OpenSearchHandler(logging.Handler):
    _client = Client().get()

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self._client.index(index="logs", body=json.loads(log_entry), refresh=True)
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
        except Exception as e:
            logging.error(f"Failed to send log to OpenSearch: {e}")


class OpenSearchFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        return json.dumps(log_record)


class OpenSearchChatLogger:
    def __init__(self):
        self._client = Client().get()
        self.index_name = "chat_logs"

    def log_chat_context(self, document_ids: list[int], query: str, file: UploadFile):
        is_file = False if file is None else True
        document = {
            "embed": bool(document_ids),
            "web": bool(extract_urls(query)),
            "file": is_file,
            "timestamp": datetime.now().isoformat(),
        }
        response = self._client.index(index=self.index_name, body=document)
        return response


opensearch_chat_logger = OpenSearchChatLogger()


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
            settings = get_settings()
            # TODO: OpenSearch
            cls.logs_directory = Path(root_directory) / "logs"
            cls.logs_directory.mkdir(parents=True, exist_ok=True)
            cls.log_level = logging.DEBUG if settings.DEBUG else logging.INFO
            cls.initialized = True  # 이제 클래스가 초기화되었다고 표시

    @staticmethod
    def get_handler(handler_type):
        if not LoggerHandler.initialized:
            LoggerHandler._initialize()  # 핸들러 요청 시 클래스가 초기화되었는지 확인

        if handler_type == "opensearch":
            handler = OpenSearchHandler()
            formatter = OpenSearchFormatter()
        else:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
        handler.setLevel(LoggerHandler.log_level)
        handler.setFormatter(formatter)
        return handler


def set_logger(logger_name="surromind-ai-chatbot-server"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(LoggerHandler.log_level if LoggerHandler.initialized else logging.INFO)
    logger.addHandler(LoggerHandler.get_handler("console"))
    logger.addHandler(LoggerHandler.get_handler("opensearch"))


set_logger()  # 로거 설정


def get_logger(logger_name="surromind-ai-chatbot-server"):
    return logging.getLogger(logger_name)
