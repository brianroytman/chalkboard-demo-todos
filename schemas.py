from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TodoModel(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    user_id: int
    date_created: datetime
    date_updated: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class TodoCreateModel(BaseModel):
    title: str
    description: str
    is_completed: bool
    user_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "title": "test title",
                "description": "test description",
                "is_completed": False,
                "user_id": 1111
            }
        }
    )

class TodoUpdateModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    is_completed: Optional[bool]
    user_id: Optional[int]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "title": "test title",
                "description": "test description",
                "is_completed": False,
                "user_id": 1111
            }
        }
    )