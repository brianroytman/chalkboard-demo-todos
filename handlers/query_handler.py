from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Todo
from queries import GetTodosByUserQuery
from exceptions.user_not_found_exception import UserNotFoundException
from services.todos_service import TodoService

class TodoQueryHandler:
    def __init__(self):
        self.todos_service = TodoService()
    
    async def handle_get_todos_by_user_query(self, query: GetTodosByUserQuery, session: AsyncSession) -> list[Todo]:
        user_exists = await self.todos_service.check_user_exists(query.user_id)
        
        if not user_exists:
            raise UserNotFoundException(f"User with id {query.user_id} not found")
        
        result = await session.execute(select(Todo).filter(Todo.user_id == query.user_id))
        return result.scalars().all()
