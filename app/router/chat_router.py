from fastapi import APIRouter,Request,Depends
from app.controllers.chat_controller import ChatController
import asyncpg
from app.db.deps import get_conn_dependency
from pydantic import BaseModel
chat_router = APIRouter(prefix="/ai-chat", tags=["Ai-Bot"])

class ChatMessege(BaseModel):
    user_query : str

@chat_router.post("/chat")
async def add_chat(request : Request,payload : ChatMessege, conn : asyncpg.Connection = Depends(get_conn_dependency)):
    controller = ChatController(conn)
    user = request.state.user
    user_id = user["id"]
    user_role = user["role"]
    print(user_id)
    print(user_role)
    print(payload.user_query)
    # return {"message" : "hello"}
    return await controller.add_chat(user_id=user_id,role=user_role,user_query=payload.user_query)

@chat_router.get("/chat/history")
async def get_chat_history(request:Request,conn : asyncpg.Connection = Depends(get_conn_dependency)):
    controller = ChatController(conn)
    user = request.state.user
    user_id = user["id"]

    return await controller.get_history(user_id=user_id) 