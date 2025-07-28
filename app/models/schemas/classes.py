from pydantic import BaseModel,ConfigDict
from typing import Optional

class ClassCreate(BaseModel):
    name: str
    section: str

class AssignTeacherToClass(BaseModel):
    teacher_id: int
    class_id: int


class ClassOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    section: str
    teacher_id: Optional[int] = None  # initially can be null
