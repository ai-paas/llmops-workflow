import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.responses import Response

from core.loggers import get_logger
from fastapi import Request
from starlette.responses import JSONResponse

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: ASGIApp) -> Response:
        """
        API 요청을 로깅하고, 커스텀 예외를 처리하며, 기타 예외를 로깅하는 미들웨어 함수입니다.

        Args:
            request (Request): 들어오는 API 요청입니다.
            call_next (ASGIApp): 체인에서 다음 미들웨어 또는 핸들러입니다.

        Returns:
            Response: 적절한 상태 코드와 내용을 포함한 API 응답입니다.
        """
        logger = get_logger()
        start_time = time.time()

        try:
            response: Response = await call_next(request)
            process_time = time.time() - start_time
            status_code: int = response.status_code
            log_message = f"Response: {status_code} | Time: {process_time:.2f}s for {request.method} {request.url}"
            
            if status_code >= 400:
                logger.error(log_message)
            else:
                logger.info(log_message)
                
            return response
        except Exception:
            process_time = time.time() - start_time
            status_code = 500
            error_log = f"Response: {status_code} | Time: {process_time:.2f}s for {request.method} {request.url}"
            logger.error(error_log)
            
            error_response = {"detail": "문제가 발생했습니다. 관리자에게 문의해주세요."}
            return JSONResponse(status_code=500, content=error_response)
