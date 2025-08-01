from app.repositories.study_material_repo import StudyMaterialRepository
from app.repositories.class_repo import ClassRepository
from fastapi import UploadFile,Request
from app.utils.api_response import error_response
from app.models.schemas.study_materials_schema import StudyMaterialCreate,StudyMaterialsOut
import os
from app.utils.upload_file_helper import save_file

UPLOAD_DIR = "uploads/study_materials"

class StudyMaterialService:
    def __init__(self, study_material_repo : StudyMaterialRepository, class_repo : ClassRepository):
        self.study_material_repo = study_material_repo
        self.class_repo = class_repo

    async def upload_material(self,request: Request, teacher_id : int, data : StudyMaterialCreate, file : UploadFile):
        is_class_exists = await self.class_repo.get_by_id(data.class_id)
        if not is_class_exists:
            return error_response(message="Class not found", status_code=404)

        if is_class_exists["teacher_id"] != teacher_id:
            return error_response(message="Not authorized to upload for this class")
        
        
        # os.makedirs(UPLOAD_DIR, exist_ok=True)
        # file_path = os.path.join(UPLOAD_DIR, file.filename)

        # with open(file_path, "wb") as f:
        #     f.write(await file.read())


        scheme = request.url.scheme
        host = request.headers.get("host")

        base_url = f"{scheme}://{host}"

        file_path, public_url= await save_file(file, UPLOAD_DIR,base_url)


        saved = await self.study_material_repo.create(
            class_id=data.class_id,
            teacher_id=data.teacher_id,
            title=data.title,
            description=data.description,
            file_path=file_path,
            public_url=public_url
        )

        json = StudyMaterialsOut(**dict(saved))


        return json
    

    async def get_study_materials_by_class(self,class_id : int)-> list[StudyMaterialsOut]:
        # [ClassOut(**dict(r)) for r in classes]
        materials = await self.study_material_repo.get_by_class(class_id)

        data = [StudyMaterialsOut(**dict(r)) for r in materials]

        return [StudyMaterialsOut(**dict(r)) for r in materials]
