
from app.repositories.subject_repository import SubjectRepository

class SubjectService:
    def __init__(self,subject_repo : SubjectRepository):
        self.subject_repo = subject_repo

    async def get_subjects(self):
        result = await self.subject_repo.get_subjects() 
        print(result)
        return [dict(r) for r in result] 
        