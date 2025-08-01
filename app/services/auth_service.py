from fastapi import HTTPException, status
from app.repositories.auth_repo import AuthRepository
from app.utils.password_hasher import verify_password, hash_password
from app.core.security import create_access_token
from app.models.schemas.user import UserCreate, UserOut
from app.models.schemas.auth import TokenRespons
from app.utils.api_response import error_response


class AuthService:

    def __init__(self, authRepo: AuthRepository):
        self.authRepo = authRepo

    async def authenticate_user(self, email: str, password: str) -> TokenRespons:
        print(email)
        print(password)
        user = await self.authRepo.get_by_email(email)

        print(user)
        if not user or not verify_password(password, user["password"]):
            raise HTTPException(detail="Invalid Credentials" , status_code=401)
        
        
        token = create_access_token(data={"sub": str(user["id"]), "role": user["role"]})
        user_role = user["role"]
        return token,user_role

    async def register_user(self, user: UserCreate) -> UserOut:
        existing = await self.authRepo.get_by_email(user.email)

        if existing:
            raise HTTPException(detail="User already exists" , status_code=400)

        hashed_password = user.copy(update={"password": hash_password(user.password)})
        new_user = await self.authRepo.create_user(hashed_password)

        print("new_user : ",new_user)
        return UserOut(**dict(new_user))
    

    async def logout_user(self, user_id:int):
        existing = await self.authRepo.get_by_id(user_id)

        if not existing:
            return error_response(message="User does not exists" , status_code=400)
        return 
