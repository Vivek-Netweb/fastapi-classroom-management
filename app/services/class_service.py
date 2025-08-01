from app.repositories.class_repo import ClassRepository

class ClassService:
    def __init__(self, class_repo : ClassRepository):
        self.class_repo = class_repo


    async def get_class_by_teacher(self, teacher_id : int):
        return await self.class_repo.get_class_by_teacher_id(teacher_id)

        