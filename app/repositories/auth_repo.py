from app.db.database import Database
from app.utils.password_hasher import hash_password
from app.models.schemas.user import UserCreate
import asyncpg

class AuthRepository:

    def __init__(self,conn: asyncpg.Connection):
        self.conn = conn
        

    async def get_by_email(self, email:str):
        query = "SELECT id, email, full_name, role, is_active, password, created_at FROM users WHERE email=$1"
        return await self.conn.fetchrow(query,email)
    
    async def get_by_id(self, user_id:int):
        query = "SELECT * FROM users WHERE id=$1"
        return await self.conn.fetchrow(query,user_id)
    
    async def create_user(self, user : UserCreate):
        query = """
        INSERT INTO users (email, password, full_name, role)
        VALUES ($1, $2, $3, $4)
        RETURNING id, email, full_name, role, is_active, created_at
        """
        # hashed = hash_password(user.password)
        return await self.conn.fetchrow(query, user.email, user.password, user.full_name, user.role)
