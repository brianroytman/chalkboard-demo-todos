import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import TodoCreateModel, TodoUpdateModel
from models import Todo
from repositories.todos_repository import TodoRepository
from exceptions.user_not_found_exception import UserNotFoundException


class TodoService:
    def __init__(self):
        self.todo_repository = TodoRepository()

    async def find_user_by_id(user_id: int):
        url = "http://localhost:8001/users/{user_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url.format(user_id=user_id))
            response.raise_for_status()  # Raise exception for non-2xx responses
            return response.json()

    async def create_todo(self, todo_data: TodoCreateModel, session: AsyncSession) -> Todo:
        # Validate user_id exists
        user = await TodoService.find_user_by_id(todo_data.user_id)
        if not user:
            raise UserNotFoundException(todo_data.user_id)

        # Proceed with creating todo
        new_todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            user_id=todo_data.user_id
        )
        return await self.todo_repository.create(session, new_todo)

    async def get_todo(self, todo_id: int, session: AsyncSession) -> Todo:
        return await self.todo_repository.get_by_id(session, todo_id)

    async def get_todos(self, session: AsyncSession) -> list[Todo]:
        return await self.todo_repository.get_all(session)

    async def update_todo(self, todo_id: int, todo_data: TodoUpdateModel, session: AsyncSession) -> Todo:
        # Validate user_id exists
        user = await TodoService.find_user_by_id(todo_data.user_id)
        if not user:
            raise UserNotFoundException(todo_data.user_id)

        # Retrieve the todo to update
        todo = await self.todo_repository.get_by_id(session, todo_id)
        if not todo:
            raise ValueError(f"Todo with ID {todo_id} not found.")

        # Persist changes
        return await self.todo_repository.update(session, todo_id, todo_data.model_dump())

    async def delete_todo(self, todo_id: int, session: AsyncSession) -> None:
        return await self.todo_repository.delete(session, todo_id)

    async def get_user_todos(self, user_id: int, session: AsyncSession) -> list[Todo]:
        return await self.todo_repository.get_user_todos_by_id(session, user_id)
