from fastapi import APIRouter, Request, Depends
from app.middlewares.role_based_access import required_roles
from app.controllers.user_controller import UserController
import asyncpg
from app.db.deps import get_conn_dependency

user_routes = APIRouter(prefix="/users", tags=["Dashboard"])


# Authenticated User
@user_routes.get("/profile")
async def get_profile(request: Request):
    user = request.state.user
    print("user auth")

    return {
        "message": "Authenticated User",
        "user_id": user["id"],
        "role": user["role"],
    }


# Authorized User
@user_routes.get("/user-profile")
async def get_profile(
    request: Request, conn: asyncpg.Connection = Depends(get_conn_dependency)
):
    user = request.state.user
    print("user auth")
    user_controller = UserController(conn)

    print(type(user["id"]))

    return await user_controller.get_user_by_id(user["id"])
    # return


@user_routes.get("/")
async def get_all_users(
    request: Request,
    _: None = Depends(required_roles(["admin"])),
    conn: asyncpg.Connection = Depends(get_conn_dependency),
):
    controller = UserController(conn)
    return await controller.get_all_user()
