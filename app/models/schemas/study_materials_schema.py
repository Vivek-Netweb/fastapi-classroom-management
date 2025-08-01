from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class StudyMaterialCreate(BaseModel):
    title: str
    description: Optional[str] = None
    class_id: int
    teacher_id: int


class StudyMaterialsOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, 
        json_encoders={datetime: lambda v: v.isoformat()}
    )

    id: int
    class_id: int
    teacher_id: int
    title: str
    description: Optional[str]
    file_path: str
    public_url: str
    uploaded_at: datetime
