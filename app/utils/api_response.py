from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import status
from app.models.schemas.api_response import APIError, APIResponse
from typing import Dict, Optional,List


def success_response(
    data=None,
    message="sucess",
    status_code=status.HTTP_200_OK,
    cookies: Optional[Dict[str, str]] = None,
    delete_cookies: Optional[List[str]] = None
):
    
    if hasattr(data, "model_dump"):
        data = data.model_dump(mode="json")
    content = APIResponse(
        success=True, message=message, data=data, status_code=status_code
    ).dict()

    response = JSONResponse(status_code=status_code, content=content)

    if cookies:
        print("cookies", cookies)
        for key, value in cookies.items():
            print(key, value)
            response.set_cookie(
                key=key,
                value=value,
                httponly=True,
                secure=False,      # True for production (HTTPS)
                samesite="Lax",
                max_age=3600,
                path="/"
            )
    if delete_cookies:
        for key in delete_cookies:
            response.delete_cookie(key)


    return response

def error_response(
    message="error", error=None, status_code=status.HTTP_400_BAD_REQUEST, delete_cookies : Optional[List[str]] = None
):
    
    content=APIError(success=False, message=message, error=error, status_code=status_code).dict()
        
    response = JSONResponse(status_code=status_code,content=content)
    if delete_cookies:
        for key in delete_cookies:
            response.delete_cookie(key)

    return response

