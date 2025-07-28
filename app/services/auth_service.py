from fastapi import HTTPException, status
from app.repositories.auth_repo import AuthRepository
from app.utils.password_hasher import verify_password, hash_password
from app.core.security import create_access_token
from app.models.schemas.user import UserCreate, UserOut
from app.models.schemas.auth import TokenRespons


class AuthService:

    def __init__(self, authRepo: AuthRepository):
        self.authRepo = authRepo

    async def authenticate_user(self, email: str, password: str) -> TokenRespons:
        user = await self.authRepo.get_by_email(email)

        if not user or not verify_password(password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
            )
        
        print("why cookie is generating")
        token = create_access_token(data={"sub": str(user["id"]), "role": user["role"]})
        print("token")
        return TokenRespons(access_token=token, token_type="bearer")

    async def register_user(self, user: UserCreate) -> UserOut:
        existing = await self.authRepo.get_by_email(user.email)

        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = user.copy(update={"password": hash_password(user.password)})
        new_user = await self.authRepo.create_user(hashed_password)

        print("new_user : ",new_user)
        return UserOut(**dict(new_user))
    

    async def logout_user(self, user_id:int):
        existing = await self.authRepo.get_by_id(user_id)

        if not existing:
            raise HTTPException(status_code=400, detail="User does not exists")
        return 
