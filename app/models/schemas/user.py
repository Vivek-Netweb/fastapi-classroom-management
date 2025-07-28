from pydantic import BaseModel, EmailStr,ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime

class UserRole(str,Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class UserCreate(BaseModel):
    email : EmailStr
    password : str
    full_name : str
    role : UserRole

class UserLogin(BaseModel):
    id : int
    email : EmailStr
    full_name : str
    role : UserRole

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True,json_encoders={
            datetime: lambda v: v.isoformat(),
            UserRole: lambda v: v.value,
        })

    id : int
    email : EmailStr
    full_name : str
    role : UserRole
    is_active: bool
    created_at: datetime
