import os
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import TodoCreateModel, TodoUpdateModel
from models import Todo
from repositories.todos_repository import TodoRepository
from exceptions.user_not_found_exception import UserNotFoundException


class TodoService:
    def __init__(self):
        self.todo_repository = TodoRepository()

    async def find_user_by_id(self, user_id: int):
        base_url = os.getenv('USERS_SERVICE_URL', 'http://localhost:8001')
        url = f"{base_url}/users/{user_id}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()  # Raise exception for non-2xx responses
                return response.json() if response.status_code == 200 else None
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None  # User not found
                else:
                    raise  # Raise other HTTP status errors
            except httpx.RequestError:
                raise  # Handle network or request errors
        
    async def check_user_exists(self, user_id: int):
        user_data = await self.find_user_by_id(user_id)
        return user_data is not None

    async def create_todo(self, todo_data: TodoCreateModel, session: AsyncSession) -> Todo:
        # Validate user_id exists
        user = await self.find_user_by_id(todo_data.user_id)
        if not user:
            raise UserNotFoundException(todo_data.user_id)

        # Proceed with creating todo
        new_todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            user_id=todo_data.user_id
        )
        return await self.todo_repository.add(session, new_todo)

    async def get_todo(self, todo_id: int, session: AsyncSession) -> Todo:
        return await self.todo_repository.get_by_id(session, todo_id)

    async def get_todos(self, session: AsyncSession) -> list[Todo]:
        return await self.todo_repository.get_all(session)

    async def update_todo(self, todo_id: int, todo_data: TodoUpdateModel, session: AsyncSession) -> Todo:
        # Validate user_id exists
        user = await self.find_user_by_id(todo_data.user_id)
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
