import asyncpg
from fastapi import HTTPException
from app.services.admin_service import AdminService
from app.services.subject_service import SubjectService
from app.repositories.admin_repo import AdminRepository
from app.repositories.auth_repo import AuthRepository
from app.repositories.subject_repository import SubjectRepository
from app.models.schemas.classes import ClassCreate,AssignTeacherToClass
from app.models.schemas.subject import SubjectCreate
from app.utils.api_response import success_response,error_response
from app.logger.logger import logger

class AdminController:
    def __init__(self, conn : asyncpg.Connection):
        self.admin_service = AdminService(AdminRepository(conn),AuthRepository(conn))
        self.subject_service = SubjectService(SubjectRepository(conn))

    async def create_class(self, payload :ClassCreate):
        try:
            result = await self.admin_service.create_class(payload)
            return success_response(result, message="Claass Created Successfully", status_code=201)
        except HTTPException as e:
            return error_response(message=e.detail, status_code=e.status_code)
        except Exception as e:
            return error_response(message="Internal Server Error", error=str(e), status_code=500)
        

    async def create_subject(self, payload :SubjectCreate):
        try:
            result = await self.admin_service.create_subject(payload)
            return success_response(result, message="Subject Created Successfully", status_code=201)
        except HTTPException as e:
            return error_response(message=e.detail, status_code=e.status_code)
        except Exception as e:
            return error_response(message="Internal Server Error", error=str(e), status_code=500)
        
    async def assign_teacher_to_class(self, payload :AssignTeacherToClass):
        try:
            result = await self.admin_service.assign_teacher_to_class(payload)
            return success_response(result, message="Teacher Assigned to a Class", status_code=201)
        except HTTPException as e:
            return error_response(message=e.detail, status_code=e.status_code)
        except Exception as e:
            return error_response(message="Internal Server Error", error=str(e), status_code=500)
        
    async def get_all_classes(self):
        try:
            result = await self.admin_service.get_all_classes()
            return success_response(message="Fetched", data=result, status_code=200)
        except HTTPException as e:
            return error_response(message=e.detail, status_code=e.status_code)
        except Exception as e:
            return error_response(message="Internal Server Error", error=str(e), status_code=500)
        
    async def get_all_subjects(self):
        try:
            result = await self.subject_service.get_subjects()
            return success_response(message="Fetched", data=result, status_code=200)
        except HTTPException as e:
            return error_response(message=e.detail, status_code=e.status_code)
        except Exception as e:
            return error_response(message="Internal Server Error", error=str(e), status_code=500)
        
    async def get_all_teachers(self):
        try:
            result = await self.admin_service.get_all_teachers()
            return success_response(message="Fetched", data=result, status_code=200)
        except HTTPException as e:
            return error_response(message=e.detail, status_code=e.status_code)
        except Exception as e:
            return error_response(message="Internal Server Error", error=str(e), status_code=500)