from fastapi import APIRouter,Depends,Response, HTTPException,Request
from fastapi.responses import JSONResponse
import asyncpg
from app.middlewares.role_based_access import required_roles
from app.db.deps import get_conn_dependency
from app.controllers.auth_controller import AuthController
from app.models.schemas.auth import LoginRequest,TokenRespons
from app.models.schemas.user import UserCreate
from app.utils.api_response import success_response,error_response
auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/login")
async def login_user(payload : LoginRequest, conn : asyncpg.Connection = Depends(get_conn_dependency)):
    controller = AuthController(conn)
    return await controller.login(payload)



@auth_router.post("/register")
async def regiser_user(user : UserCreate, conn : asyncpg.Connection = Depends(get_conn_dependency)):
    controller = AuthController(conn)
    return await controller.register(user)

@auth_router.post("/create-user")
async def regiser_user(user : UserCreate, _:None = Depends(required_roles(["admin"])),conn : asyncpg.Connection = Depends(get_conn_dependency)):
    controller = AuthController(conn)
    return await controller.register(user)


@auth_router.delete("/logout")
async def logut_user(request: Request, response : Response,conn : asyncpg.Connection = Depends(get_conn_dependency)):
    user = request.state.user
    user_id = user["id"]
    print(user_id)
    controller = AuthController(conn)
    return await controller.logout(user_id)
    # print(result)
    # response = JSONResponse(content=result, status_code=200)
    # response.delete_cookie(key="access_token", path="/")
    return response