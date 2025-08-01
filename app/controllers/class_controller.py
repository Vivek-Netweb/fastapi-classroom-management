import asyncpg
from app.utils.api_response import success_response,error_response
from app.repositories.class_repo import ClassRepository
from app.services.class_service import ClassService
class ClassController:
    def __init__(self,  conn : asyncpg.Connection):
        self.class_service = ClassService(ClassRepository(conn))

    
    async def get_assigned_class(self, teacher_id : int):
        data = await self.class_service.get_class_by_teacher(teacher_id)
        return success_response(data=data,message="Class fetched Successfully",status_code=200)