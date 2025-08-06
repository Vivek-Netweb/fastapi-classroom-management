import asyncpg
from typing import List, Dict, Any
import json


class ChatRepository:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def save_user_message(self, user_id: int, role: str, message: str):
        query = """
                INSERT INTO chat_history (user_id, role, message)
                VALUES ($1,$2,$3)
                """

        return await self.conn.execute(query, user_id, role, message)

    async def save_ai_message(
        self,
        user_id: int,
        role: str,
        user_query: str,
        title: str,
        explanation: str,
        point,
    ):
        query = """
                INSERT INTO chat_history (user_id, role, message, title, explanation, points)
                VALUES ($1, $2, $3, $4, $5, $6)
                """

        rows = await self.conn.execute(
            query, user_id, role, user_query, title, explanation, json.dumps(point)
        )

        return
    
    async def get_all_messages(self, user_id:int):
        query = """
                SELECT * FROM chat_history WHERE user_id = $1
                """
        rows = await self.conn.fetch(query,user_id)

        return [dict(row) for row in rows]
