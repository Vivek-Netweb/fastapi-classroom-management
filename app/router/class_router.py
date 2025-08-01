from fastapi import APIRouter, File, Form, UploadFile, Depends,Request
from app.controllers.class_controller import ClassController
from app.models.schemas.study_materials_schema import StudyMaterialCreate
from app.db.deps import get_conn_dependency
import asyncpg

class_router = APIRouter(prefix="/class", tags=["Class"])

@class_router.get("/assigned-class")
async def get_assigned_class(request: Request,conn: asyncpg.Connection = Depends(get_conn_dependency)):
    user = request.state.user
    controller = ClassController(conn)
    print(user["id"])
    return await controller.get_assigned_class(user["id"])

