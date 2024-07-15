from models import Todo
from commands import CreateTodoCommand
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.todos_repository import TodoRepository
from services.todos_service import TodoService
from exceptions.user_not_found_exception import UserNotFoundException

class TodoCommandHandler:
    def __init__(self):
        self.todos_service = TodoService()

    async def handle_create_todo_command(self, command: CreateTodoCommand, session: AsyncSession) -> Todo:
        user_exists = await self.todos_service.check_user_exists(command.user_id)

        if not user_exists:
            raise UserNotFoundException(f"User with id {command.user_id} not found")

        new_todo = Todo(
            title=command.title,
            description=command.description,
            is_completed=command.is_completed,
            user_id=command.user_id
        )
        session.add(new_todo)
        await session.commit()
        await session.refresh(new_todo)
        return new_todo