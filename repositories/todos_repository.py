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