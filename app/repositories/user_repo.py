import asyncpg
from typing import List, Optional, Dict


class UserRepository:
    def __init__(self, conn : asyncpg.Connection):
        self.conn = conn

    async def get_all_users(self):
        query = "SELECT id, email, role, full_name FROM users ORDER BY id"
        result = await self.conn.fetch(query)
        return [dict(row) for row in result]

    async def get_user_by_id(self, user_id:int) -> Optional[Dict]:
        query = "SELECT id, email, role, full_name FROM users WHERE id = $1"
        result =  await self.conn.fetchrow(query, user_id)
        return dict(result) if result else None
    
    async def delete_user(self,user_id) -> bool:
        query = "DELETE FROM users WHERE id = $1"
        result = await self.conn.execute(query, user_id)
        return result == "DELETE 1"
    
