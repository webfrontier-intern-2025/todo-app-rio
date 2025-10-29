from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TodoBase(BaseModel):
    content: str
    complete: bool = False
    deadline: Optional[datetime] = None


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    pass


class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2対応
