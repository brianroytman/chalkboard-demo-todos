import unittest
from unittest.mock import patch, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from services.todos_service import TodoService
from schemas import TodoCreateModel, TodoUpdateModel
from models import Todo
from exceptions.user_not_found_exception import UserNotFoundException
from schemas import TodoCreateModel


class TestTodoService(unittest.IsolatedAsyncioTestCase):

    @patch('services.todos_service.TodoService.find_user_by_id')
    async def test_find_user_by_id(self, mock_find_user_by_id):
        mock_find_user_by_id.return_value = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }

        # Create TodoService instance
        todo_service = TodoService()

        # Call find_user_by_id
        user_id = 1
        result = await todo_service.find_user_by_id(user_id)

        # Assertions
        self.assertEqual(result['username'], 'testuser')
        self.assertEqual(result['email'], 'testuser@example.com')
        self.assertEqual(result['first_name'], 'Test')
        self.assertEqual(result['last_name'], 'User')

    @patch('services.todos_service.TodoService.find_user_by_id')
    async def test_create_todo(self, mock_find_user_by_id):
        mock_find_user_by_id.return_value = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }

        # Mock TodoRepository's create method with AsyncMock
        mock_repository = AsyncMock()
        mock_repository.create.return_value = Todo(
            id=1,
            title='Test Todo',
            description='Test Description',
            is_completed=False,
            user_id=1
        )

        # Create TodoService instance with mocked repository
        todo_service = TodoService()
        todo_service.todo_repository = mock_repository

        # Call create_todo
        todo_data = TodoCreateModel(
            title='Test Todo',
            description='Test Description',
            is_completed=False,
            user_id=1
        )
        session = AsyncSession()
        result = await todo_service.create_todo(todo_data, session)

        # Assertions
        self.assertEqual(result.title, 'Test Todo')
        self.assertEqual(result.description, 'Test Description')
        self.assertEqual(result.is_completed, False)
        self.assertEqual(result.user_id, 1)

    @patch('services.todos_service.TodoService.find_user_by_id')
    async def test_get_todo(self, mock_find_user_by_id):
        mock_find_user_by_id.return_value = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }

        # Mock TodoRepository's get_by_id method with AsyncMock
        mock_repository = AsyncMock()
        mock_repository.get_by_id = AsyncMock(return_value=Todo(
            id=1,
            title='Test Todo',
            description='Test Description',
            is_completed=False,
            user_id=1
        ))

        # Create TodoService instance and set the mocked repository
        todo_service = TodoService()
        todo_service.todo_repository = mock_repository

        # Call get_todo
        todo_id = 1
        result = await todo_service.get_todo(todo_id=todo_id, session=AsyncSession)

        # Assertions
        self.assertEqual(result.title, 'Test Todo')
        self.assertEqual(result.description, 'Test Description')
        self.assertEqual(result.is_completed, False)
        self.assertEqual(result.user_id, 1)

    @patch('services.todos_service.TodoService.find_user_by_id')
    async def test_update_todo(self, mock_find_user_by_id):
        mock_find_user_by_id.return_value = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }

        # Mock TodoRepository's update method with AsyncMock
        mock_repository = AsyncMock()
        mock_repository.update.return_value = Todo(
            id=1,
            title='Updated Todo',
            description='Updated Description',
            is_completed=True,
            user_id=1
        )

        # Create TodoService instance with mocked repository
        todo_service = TodoService()
        todo_service.todo_repository = mock_repository

        # Call update_todo
        todo_id = 1
        todo_data = TodoUpdateModel(
            title='Updated Todo',
            description='Updated Description',
            is_completed=True,
            user_id=1
        )
        session = AsyncSession()
        result = await todo_service.update_todo(todo_id, todo_data, session)

        # Assertions
        self.assertEqual(result.title, 'Updated Todo')
        self.assertEqual(result.description, 'Updated Description')
        self.assertEqual(result.is_completed, True)
        self.assertEqual(result.user_id, 1)

    @patch('services.todos_service.TodoService.find_user_by_id')
    async def test_delete_todo(self, mock_find_user_by_id):
        mock_find_user_by_id.return_value = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }

        # Mock TodoRepository's delete method with AsyncMock
        mock_repository = AsyncMock()
        mock_repository.delete.return_value = True

        # Create TodoService instance with mocked repository
        todo_service = TodoService()
        todo_service.todo_repository = mock_repository

        # Call delete_todo
        todo_id = 1
        session = AsyncSession()
        result = await todo_service.delete_todo(todo_id, session)

        # Assertions
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
