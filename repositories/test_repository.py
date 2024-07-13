import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status
from datetime import datetime, timezone
from models import Todo
from repositories.todos_repository import TodoRepository


class TestTodoRepository(unittest.IsolatedAsyncioTestCase):

    async def test_create_todo(self):
        # Mock AsyncSession
        mock_session = MagicMock(spec=AsyncSession)
        
        # Mock Todo object
        mock_todo = Todo(
            title='Test Todo',
            description='This is a test todo',
            is_completed=False,
            user_id=1
        )
        
        # Mock session.add() and session.commit()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        
        # Instantiate TodoRepository
        todo_repo = TodoRepository()
        
        # Call create method
        result = await todo_repo.create(mock_session, mock_todo)
        
        # Assertions
        self.assertEqual(result.title, 'Test Todo')
        self.assertEqual(result.description, 'This is a test todo')
        self.assertFalse(result.is_completed)
        self.assertEqual(result.user_id, 1)

    async def test_get_by_id_existing_todo(self):
        # Mock AsyncSession
        mock_session = MagicMock(spec=AsyncSession)
        
        # Mock Todo object
        mock_todo = Todo(
            id=1,
            title='Existing Todo',
            description='This is an existing todo',
            is_completed=False,
            user_id=1
        )
        
        # Mock session.execute() and result.scalars().one()
        mock_result = MagicMock()
        mock_result.scalars().one.return_value = mock_todo
        mock_session.execute.return_value = mock_result
        
        # Instantiate TodoRepository
        todo_repo = TodoRepository()
        
        # Call get_by_id method
        result = await todo_repo.get_by_id(mock_session, 1)
        
        # Assertions
        self.assertEqual(result.id, 1)
        self.assertEqual(result.title, 'Existing Todo')
        self.assertEqual(result.description, 'This is an existing todo')
        self.assertFalse(result.is_completed)
        self.assertEqual(result.user_id, 1)

    async def test_get_by_id_non_existing_todo(self):
        # Mock AsyncSession
        mock_session = MagicMock(spec=AsyncSession)
        
        # Mock session.execute() and result.scalars().one()
        mock_result = MagicMock()
        mock_result.scalars().one.side_effect = NoResultFound
        mock_session.execute.return_value = mock_result
        
        # Instantiate TodoRepository
        todo_repo = TodoRepository()
        
        # Call get_by_id method and expect HTTPException
        with self.assertRaises(HTTPException) as context:
            await todo_repo.get_by_id(mock_session, 999)
        
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, 'Todo not found')

    async def test_get_all_todos(self):
        # Mock AsyncSession
        mock_session = MagicMock(spec=AsyncSession)
        
        # Mock Todo objects
        mock_todos = [
            Todo(
                id=1,
                title='Todo 1',
                description='This is todo 1',
                is_completed=False,
                user_id=1
            ),
            Todo(
                id=2,
                title='Todo 2',
                description='This is todo 2',
                is_completed=True,
                user_id=1
            )
        ]
        
        # Mock session.execute() and result.scalars().all()
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = mock_todos
        mock_session.execute.return_value = mock_result
        
        # Instantiate TodoRepository
        todo_repo = TodoRepository()
        
        # Call get_all method
        results = await todo_repo.get_all(mock_session)
        
        # Assertions
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].id, 1)
        self.assertEqual(results[0].title, 'Todo 1')
        self.assertEqual(results[0].description, 'This is todo 1')
        self.assertFalse(results[0].is_completed)
        self.assertEqual(results[0].user_id, 1)
        self.assertEqual(results[1].id, 2)
        self.assertEqual(results[1].title, 'Todo 2')
        self.assertEqual(results[1].description, 'This is todo 2')
        self.assertTrue(results[1].is_completed)
        self.assertEqual(results[1].user_id, 1)

    async def test_update_todo(self):
        # Mock AsyncSession
        mock_session = MagicMock(spec=AsyncSession)
        
        # Mock Todo object
        mock_todo = {
            'title': 'Updated Title',
            'description': 'This is an updated todo',
            'is_completed': True,
            'user_id': 1
        }
        
        # Mock session.execute() and result.scalar()
        mock_result = MagicMock()
        mock_result.scalar.return_value = Todo(
            id=1,
            title='Existing Todo',
            description='This is an existing todo',
            is_completed=False,
            user_id=1
        )
        mock_session.execute.return_value = mock_result
        
        # Instantiate TodoRepository
        todo_repo = TodoRepository()
        
        # Call update method
        result = await todo_repo.update(mock_session, 1, mock_todo)
        
        # Assertions
        self.assertEqual(result.title, 'Updated Title')
        self.assertEqual(result.description, 'This is an updated todo')
        self.assertTrue(result.is_completed)
        self.assertEqual(result.user_id, 1)

    async def test_delete_todo(self):
        # Mock AsyncSession
        mock_session = MagicMock(spec=AsyncSession)
        
        # Mock Todo object to be deleted
        mock_todo = Todo(
            id=1,
            title='Existing Todo',
            description='This is an existing todo',
            is_completed=False,
            user_id=1
        )
        
        # Mock session.execute() and result.scalars().one()
        mock_result = MagicMock()
        mock_result.scalars().one.return_value = mock_todo
        mock_session.execute.return_value = mock_result
        
        # Instantiate TodoRepository
        todo_repo = TodoRepository()
        
        # Call delete method
        await todo_repo.delete(mock_session, 1)
        
        # Assertions
        mock_session.execute.assert_called_once()  # Ensure execute was called once
        mock_result.scalars().one.assert_called_once()  # Ensure scalars().one() was called once
        mock_session.delete.assert_called_once_with(mock_todo)  # Ensure delete was called with the correct Todo object
        mock_session.commit.assert_called_once()  # Ensure commit was called once

    async def test_get_user_todos_by_id(self):
        # Mock AsyncSession
        mock_session = MagicMock(spec=AsyncSession)
        
        # Mock Todo objects
        mock_todos = [
            Todo(
                id=1,
                title='Todo 1',
                description='This is todo 1',
                is_completed=False,
                user_id=1
            ),
            Todo(
                id=2,
                title='Todo 2',
                description='This is todo 2',
                is_completed=True,
                user_id=1
            )
        ]
        
        # Mock session.execute() and result.scalars().all()
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = mock_todos
        mock_session.execute.return_value = mock_result
        
        # Instantiate TodoRepository
        todo_repo = TodoRepository()
        
        # Call get_user_todos_by_id method
        results = await todo_repo.get_user_todos_by_id(mock_session, 1)
        
        # Assertions
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].id, 1)
        self.assertEqual(results[0].title, 'Todo 1')
        self.assertEqual(results[0].description, 'This is todo 1')
        self.assertFalse(results[0].is_completed)
        self.assertEqual(results[0].user_id, 1)
        self.assertEqual(results[1].id, 2)
        self.assertEqual(results[1].title, 'Todo 2')
        self.assertEqual(results[1].description, 'This is todo 2')
        self.assertTrue(results[1].is_completed)
        self.assertEqual(results[1].user_id, 1)

if __name__ == '__main__':
    unittest.main()


