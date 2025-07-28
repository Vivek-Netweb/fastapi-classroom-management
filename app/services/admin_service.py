from app.models.schemas.classes import ClassCreate, AssignTeacherToClass, ClassOut
from app.models.schemas.subject import SubjectCreate
from app.repositories.admin_repo import AdminRepository
from app.models.schemas.user import UserOut

from app.repositories.auth_repo import AuthRepository
from app.utils.api_response import error_response
from fastapi import HTTPException


class AdminService:
    def __init__(self, admin_repo: AdminRepository, auth_repo: AuthRepository):
        self.admin_repo = admin_repo
        self.auth_repo = auth_repo

    async def create_class(self, data: ClassCreate):
        new_class = await self.admin_repo.create_class(data)
        return ClassOut(**dict(new_class))

    async def create_subject(self, data: SubjectCreate):
        print(data.class_id)
        is_class_exists = await self.admin_repo.get_class_by_id(data.class_id)

        if not is_class_exists:
            raise HTTPException(status_code=404, detail="Class not found")

        print("helloo")
        new_subject = await self.admin_repo.create_subject(data)
        return SubjectCreate(**dict(new_subject))

    async def assign_teacher_to_class(self, data: AssignTeacherToClass):
        is_class_exists = await self.admin_repo.get_class_by_id(data.class_id)

        if not is_class_exists:
            raise HTTPException(status_code=404, detail="Class not found")

        is_teacher_exists = await self.auth_repo.get_by_id(data.teacher_id)

        if not is_teacher_exists:
            raise HTTPException(status_code=404, detail="Teacher not found")

        is_teacher_role = UserOut(**dict(is_teacher_exists))
        print(is_teacher_role.role)

        if not is_teacher_role.role == "teacher":
            raise HTTPException(
                status_code=404, detail="You cant be assign to as a class teacher"
            )

        result = await self.admin_repo.assign_teacher_to_class(
            data.teacher_id, data.class_id
        )

        return ClassOut(**dict(result))
