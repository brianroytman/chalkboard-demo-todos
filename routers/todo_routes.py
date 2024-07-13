from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_session
from schemas import TodoModel, TodoCreateModel
from services.todos_service import TodoService

router = APIRouter()

todos_service = TodoService()

@router.post("/todos", status_code=status.HTTP_201_CREATED, response_model=TodoModel)
async def create_todo(todo_data: TodoCreateModel, session: AsyncSession = Depends(get_session)):
    try:
        todo = await todos_service.create_todo(todo_data, session)
        return todo
    except Exception as e:
        await session.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))