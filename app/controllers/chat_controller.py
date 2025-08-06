from app.utils.api_response import success_response
import asyncpg
from app.services.chat_service import ChatService
from app.repositories.chat_repo import ChatRepository
from fastapi import HTTPException
class ChatController:
    def __init__(self, conn : asyncpg.Connection):
        self.chat_service = ChatService(ChatRepository(conn))

    async def add_chat(self,user_id,role,user_query):
        response = await self.chat_service.add_chat(user_id,role,user_query)
        print(response)

        return success_response(message="Sent",data=response)
    async def get_chats(self,user_id):
        response = await self.chat_service.get_chats(user_id)
        print(response)
        return success_response(message="Sent")
    
    async def get_history(self, user_id: int) -> dict:
        try:
            print(user_id)
            history = await self.chat_service.get_chats(user_id)

            return success_response(data=history)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))