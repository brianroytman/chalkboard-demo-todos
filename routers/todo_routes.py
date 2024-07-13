from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_session
from schemas import TodoModel, TodoCreateModel
from services.todos_service import TodoService
from exceptions.user_not_found_exception import UserNotFoundException
from typing import List

router = APIRouter()

todos_service = TodoService()

@router.post("/todos", status_code=status.HTTP_201_CREATED, response_model=TodoModel)
async def create_todo(todo_data: TodoCreateModel, session: AsyncSession = Depends(get_session)):
    try:
        todo = await todos_service.create_todo(todo_data, session)
        return todo
    except UserNotFoundException as unfe:
        await session.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(unfe))
    except Exception as e:
        await session.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoModel)
async def get_todo(todo_id: int, session: AsyncSession = Depends(get_session)):
    try:
        todo = await todos_service.get_todo(todo_id, session)
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        return todo
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/todos", status_code=status.HTTP_200_OK, response_model=List[TodoModel])
async def get_todos(session: AsyncSession = Depends(get_session)):
    try:
        todos = await todos_service.get_todos(session)
        return todos
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/todos/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoModel)
async def update_todo(todo_id: int, todo_data: TodoCreateModel, session: AsyncSession = Depends(get_session)):
    try:
        todo = await todos_service.update_todo(todo_id, todo_data, session)
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        return todo
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, session: AsyncSession = Depends(get_session)):
    try:
        await todos_service.delete_todo(todo_id, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))