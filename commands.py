from pydantic import BaseModel

class CreateTodoCommand(BaseModel):
    title: str
    description: str
    is_completed: bool
    user_id: int