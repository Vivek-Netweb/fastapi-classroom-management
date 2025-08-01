from pydantic import BaseModel,ConfigDict
from typing import Optional

class ClassCreate(BaseModel):
    name: str
    section: str

class AssignTeacherToClass(BaseModel):
    teacher_id: int
    class_id: int

class TeacherOut(BaseModel):
    id: Optional[int] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

class ClassOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    section: str
    teacher_id: Optional[int] = None  # initially can be null
    teacher: Optional[TeacherOut] = None
