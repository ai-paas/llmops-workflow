from fastapi import HTTPException, status


class BaseCustomException(HTTPException):
    """
    Base custom exception class that extends FastAPI's HTTPException.

    Attributes:
        status_code (int): The HTTP status code for the exception.
        detail (str): The detail message for the exception.

    Usage:
    To create a custom exception, inherit from this base class and specify the `status_code`
    and `detail` attributes for your specific exception. Then, you can raise your custom
    exception within your application.

    Example:
    class MyCustomException(BaseCustomException):
        status_code = 400
        detail = "My custom exception message"
    """

    status_code: int
    detail: str

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ItemNotFoundException(BaseCustomException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Item NotFound"


class InsertDocumentException(BaseCustomException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "문서 등록 실패! Data Rollback"


class InvalidDocumentNameException(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = """유효하지 않은 이름 입니다. :
    이름은 영문 소문자로 시작해야 하며, 사용할 수 있는 문자는 영문 소문자, 숫자, 언더스코어(_)만 사용할 수 있습니다.
    다음과 같은 특수문자는 사용할 수 없습니다. (\", *, +, /, \\, |, ?, #, >, <")
    """
