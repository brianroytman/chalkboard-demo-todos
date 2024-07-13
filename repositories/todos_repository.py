from sqlalchemy.ext.asyncio import AsyncSession
from models import Todo
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, timezone
from fastapi import HTTPException, status


class TodoRepository:
    async def create(self, session: AsyncSession, todo: Todo) -> Todo:
        session.add(todo)
        await session.commit()
        return todo

    async def get_by_id(self, session: AsyncSession, todo_id: int) -> Todo:
        statement = select(Todo).filter(Todo.id == todo_id)
        result = await session.execute(statement)
        try:
            return result.scalars().one()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    async def get_all(self, session: AsyncSession) -> list[Todo]:
        statement = select(Todo).order_by(Todo.id)
        result = await session.execute(statement)
        return result.scalars().all()

    async def update(self, session: AsyncSession, todo_id: int, data: dict) -> Todo:
        statement = select(Todo).filter(Todo.id == todo_id)
        result = await session.execute(statement)
        try:
            todo = result.scalars().one()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

        for key, value in data.items():
            setattr(todo, key, value)
        todo.date_updated = datetime.now(timezone.utc)
        await session.commit()
        return todo

    async def delete(self, session: AsyncSession, todo_id: int) -> None:
        statement = select(Todo).filter(Todo.id == todo_id)
        result = await session.execute(statement)
        try:
            todo = result.scalars().one()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

        await session.delete(todo)
        await session.commit()

    async def get_user_todos(self, session: AsyncSession, user_id: int) -> list[Todo]:
        statement = select(Todo).filter(
            Todo.user_id == user_id).order_by(Todo.id)
        result = await session.execute(statement)
        return result.scalars().all()
