from typing import Any,Optional
from fastapi import status
from pydantic import BaseModel

class APIResponse(BaseModel):
    success : bool = True
    message : str = "success"
    data : Optional[Any] = None
    status_code : int = status.HTTP_200_OK

class APIError(BaseModel):
    success : bool = False
    message : str = "something went wrong"
    error : Optional[Any] = None
    status_code : int = status.HTTP_400_BAD_REQUEST
