from fastapi import APIRouter, File, Form, UploadFile, Depends,Request
from app.controllers.study_material_controller import StudyMaterialController
from app.models.schemas.study_materials_schema import StudyMaterialCreate
from app.db.deps import get_conn_dependency
import asyncpg

study_material_router = APIRouter(prefix="/study-materials", tags=["Study Materials"])


@study_material_router.post("/upload")
async def upload_material(
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    class_id: int = Form(...),
    file: UploadFile = File(...),
    conn: asyncpg.Connection = Depends(get_conn_dependency),
):
    user = request.state.user
    controller = StudyMaterialController(conn)

    print("herererereree")
    print(user["id"])

    print(title)
    print(description)
    print(class_id)
    data = StudyMaterialCreate(title=title, description=description, class_id=class_id,teacher_id=user["id"])
    print(data)
    

    return await controller.upload(request,current_user=user["id"],data=data, file=file)


@study_material_router.get("/class/{class_id}")
async def get_class_materials(
    class_id: int,
    conn: asyncpg.Connection = Depends(get_conn_dependency)
):
    controller = StudyMaterialController(conn)
    return await controller.get_materials_by_class(class_id)