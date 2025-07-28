from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SubjectCreate(BaseModel):
    name: str
    class_id: int

class SubjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    class_id: int
    created_at: datetime
