import asyncpg
from app.services.study_materials_service import StudyMaterialService
from app.models.schemas.study_materials_schema import StudyMaterialCreate
from fastapi import UploadFile,Request
from app.utils.api_response import success_response,error_response
from app.repositories.class_repo import ClassRepository
from app.repositories.study_material_repo import StudyMaterialRepository

class StudyMaterialController:
    def __init__(self,  conn : asyncpg.Connection):
        self.study_material_service = StudyMaterialService(StudyMaterialRepository(conn), ClassRepository(conn))
    
    async def upload(self,request:Request,current_user, data : StudyMaterialCreate, file : UploadFile):
        saved = await self.study_material_service.upload_material(request,current_user, data,file)
        
        return success_response(saved,message="Material Uploaded Successfully",status_code=201)
    
    async def get_materials_by_class(self, class_id : int):
        data = await self.study_material_service.get_study_materials_by_class(class_id)
        return success_response(data=data,message="Materials fetched Successfully",status_code=200)