from sqlalchemy.ext.asyncio import AsyncSession
from schemas import TodoCreateModel
from models import Todo
from repositories.todos_repository import TodoRepository

class TodoService:
    def __init__(self):
        self.todo_repository = TodoRepository()

    async def create_todo(self, todo_data: TodoCreateModel, session: AsyncSession) -> Todo:
        new_todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            user_id=todo_data.user_id
        )
        return await self.todo_repository.create(session, new_todo)