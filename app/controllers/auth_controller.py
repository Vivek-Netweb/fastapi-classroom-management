from fastapi import HTTPException, Response
from app.models.schemas.auth import LoginRequest,TokenRespons
from app.models.schemas.user import UserCreate, UserOut
from app.services.auth_service import AuthService
from app.repositories.auth_repo import AuthRepository
import asyncpg
from app.utils.api_response import success_response, error_response


class AuthController:

    def __init__(self,conn : asyncpg.Connection):
        self.auth_service = AuthService(AuthRepository(conn))
    
    async def login(self, payload : LoginRequest):
        try:
            token = await self.auth_service.authenticate_user(payload.email, payload.password)
            cookies = {
                "access_token" : token.access_token
            }
            # logger.info()
            return success_response(data=token, message="Login Successfully!", cookies=cookies) 
        except HTTPException as e:
            raise error_response(message=e.detail, status_code=e.status_code)
        # logger.error()
        except Exception as e:
            return error_response(message="Internal Server Error", error=str(e), status_code=500)
    
    async def register(self, user : UserCreate):
        try:
            user_data = await self.auth_service.register_user(user) 
            print("user_data : ",user_data)
            return success_response(user_data, message="Register Successfully!", status_code=201)
        except HTTPException as e:
            return error_response(message=e.detail, status_code=e.status_code)
        except Exception as e:
            return error_response(message="Internal Server Error", error=str(e), status_code=500)
        

    async def logout(self, user_id : int):
        try:
            user_data = await self.auth_service.logout_user(user_id) 
            return success_response(user_data, message="Register Successfully!", status_code=200, delete_cookies=["access_token"])
        except HTTPException as e:
            return error_response(message=e.detail, status_code=e.status_code)
        except Exception as e:
            return error_response(message="Internal Server Error", error=str(e), status_code=500)
