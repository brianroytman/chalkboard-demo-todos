from pydantic import BaseModel

class GetTodosByUserQuery(BaseModel):
    user_id: int