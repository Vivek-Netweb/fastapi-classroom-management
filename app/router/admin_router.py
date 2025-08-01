from fastapi import APIRouter, Depends
from app.db.deps import get_conn_dependency
from app.middlewares.role_based_access import required_roles
from app.models.schemas.classes import ClassCreate
from app.models.schemas.classes import AssignTeacherToClass
from app.models.schemas.subject import SubjectCreate
import asyncpg
from app.controllers.admin_controller import AdminController

admin_router = APIRouter(prefix="/admin", tags=["Auth"])


@admin_router.post("/create-class")
async def create_class(payload: ClassCreate, conn: asyncpg.Connection = Depends(get_conn_dependency), _: None = Depends(required_roles(["admin"]))):
    controller = AdminController(conn)
    return await controller.create_class(payload)


@admin_router.post("/create-subject")
async def create_subject(payload: SubjectCreate, conn: asyncpg.Connection = Depends(get_conn_dependency), _: None = Depends(required_roles(["admin"]))):
    controller = AdminController(conn)
    return await controller.create_subject(payload)

@admin_router.post("/assign-teacher")
async def assign_teacher(payload: AssignTeacherToClass, conn: asyncpg.Connection = Depends(get_conn_dependency), _: None = Depends(required_roles(["admin"]))):
    controller = AdminController(conn)
    return await controller.assign_teacher_to_class(payload)

@admin_router.get("/classes")
async def get_all_classes(conn: asyncpg.Connection = Depends(get_conn_dependency), _: None = Depends(required_roles(["admin"]))):
    controller = AdminController(conn)
    return await controller.get_all_classes()

@admin_router.get("/subjects")
async def get_all_subjects(conn: asyncpg.Connection = Depends(get_conn_dependency), _: None = Depends(required_roles(["admin"]))):
    controller = AdminController(conn)
    return await controller.get_all_subjects()
@admin_router.get("/teachers")
async def get_all_teachers(conn: asyncpg.Connection = Depends(get_conn_dependency), _: None = Depends(required_roles(["admin"]))):
    controller = AdminController(conn)
    return await controller.get_all_teachers()