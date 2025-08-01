from fastapi import APIRouter,Depends,Response,Request
import asyncpg
from app.middlewares.role_based_access import required_roles
from app.db.deps import get_conn_dependency
from app.controllers.auth_controller import AuthController
from app.models.schemas.auth import LoginRequest,TokenRespons
from app.models.schemas.user import UserCreate
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