from app.repositories.user_repo import UserRepository
from fastapi import HTTPException

class UserService:
    def __init__(self, user_repo : UserRepository):
        self.user_repo = user_repo

    async def get_all_users(self):
        return await self.user_repo.get_all_users()
    
    async def get_user_by_id(self, user_id : int):
        found_user  = await self.user_repo.get_user_by_id(user_id)

        if not found_user:
            raise HTTPException(status_code=404,detail="User not found")
        return found_user
    
    async def delete_user(self, user_id : int):
        found_user  = await self.user_repo.get_user_by_id(user_id)

        if not found_user:
            raise HTTPException(status_code=404,detail="User not found")
        
        deleted_user =  await self.user_repo.delete_user(user_id)
        if not deleted_user:
            raise HTTPException(status_code=500,detail="Failed to delete user")

        return deleted_user