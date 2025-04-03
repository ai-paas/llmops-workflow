# core/response.py
from typing import Any, Dict, Optional, Union, List
from pydantic import BaseModel
from fastapi.responses import JSONResponse, FileResponse

class Pagination(BaseModel):
    page: int
    page_size: int
    total: int

class APIResponse(BaseModel):
    status: int
    message: str
    pagination: Optional[Pagination] = None
    data: Union[Dict[str, Any], List[Any], Any]

def response_formatter(
    data: Union[Dict[str, Any], List[Any], BaseModel, Any],
    status_code: int = 200,
    message: str = "success",
    pagination: Optional[Pagination] = None,
) -> Union[JSONResponse, FileResponse]:
    # Handle file response
    if isinstance(data, (bytes, str)) and hasattr(data, 'filename'):
        return FileResponse(
            data,
            filename=data.filename,
            status_code=status_code
        )
    
    # Handle Pydantic model
    if isinstance(data, BaseModel):
        data = data.model_dump()
        
    # Handle regular dict/list/other data
    response_content = APIResponse(
        status=status_code,
        message=message,
        pagination=pagination,
        data=data,
    )
    
    return JSONResponse(
        status_code=status_code,
        content=response_content.model_dump(exclude_none=True),
    )
