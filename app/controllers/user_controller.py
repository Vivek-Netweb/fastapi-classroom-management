import asyncpg
from app.services.user_service import UserService
from app.repositories.user_repo import UserRepository
from app.utils.api_response import success_response, error_response
from fastapi import HTTPException
class UserController:
    def __init__(self, conn : asyncpg.Connection):
        self.user_service = UserService(UserRepository(conn))
    
    async def get_all_user(self):
        try:
            users = await self.user_service.get_all_users()
            return success_response(users, message="Users fetched successfully")
        except HTTPException as e:
            return error_response("Error in fetching users", error=str(e), status_code=500)
        
    async def get_user_by_id(self, user_id):
        try:
            user = await self.user_service.get_user_by_id(user_id)
            print("user : ", user)
            return success_response(user, message="User fetched")
        except HTTPException as e:
            return error_response(message="Error in fetching user",error=e.detail, status_code=e.status_code)
        except Exception as e:
            return error_response(message="Internal server error", error=str(e), status_code=500)

    async def delete_user(self, user_id):
        try:
            result = await self.user_service.delete_user(user_id)
            return success_response(data=result,message="User deleted successfully",status_code=200)
        except HTTPException as e:
            return error_response(message=e.detail, status_code=e.status_code)
        except Exception as e:
            return error_response(message="Internal server error", error=str(e), status_code=500)

