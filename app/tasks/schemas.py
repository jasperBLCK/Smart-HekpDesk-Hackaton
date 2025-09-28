# схемы для задач
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


class TaskBase(BaseModel):
    title: str = Field(max_length=80)
    description: Optional[str] = Field(default=None, max_length=380)
    category: str = Field(max_length=50)
    status: str = Field(max_length=20)
    priority: str = Field(max_length=20)
    location_id: str = Field(max_length=50)
    created_by: str = Field(max_length=50)
    assigned_to: Optional[str] = Field(default=None, max_length=50)
    due_date: Optional[datetime] = None
    attachments: Optional[str] = None

class StatusPatch(BaseModel):
    status: str = Field(max_length=20)

class AssignPatch(BaseModel):
    assigned_to: Optional[str] = Field(default=None, max_length=50)


class TaskUpdate(BaseModel):
    description: Optional[str] = Field(default=None, max_length=380)
    category: Optional[str] = Field(default=None, max_length=50)
    status: Optional[str] = Field(default=None, max_length=20)
    priority: Optional[str] = Field(default=None, max_length=20)
    assigned_to: Optional[str] = Field(default=None, max_length=50)
    attachments: Optional[str] = Field(default=None, max_length=500)

class TaskRead(TaskBase):
    id: int
    created_by: str
    assigned_to: Optional[str] = None
    created_at: datetime
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)