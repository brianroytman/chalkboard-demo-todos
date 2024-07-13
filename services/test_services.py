import unittest
from unittest.mock import patch
from services.todos_service import TodoService
from schemas import TodoCreateModel, TodoModel, TodoUpdateModel
from sqlalchemy.ext.asyncio import AsyncSession

class TestTodosServices(unittest.TestCase):
    @patch('services.todos_service.TodoService.get_todo')
    async def test_create_todo(self, mock_get_todo):
        # Mock the get_todo function
        mock_get_todo.return_value = None

        # Create a new todo
        todo_service = TodoService()
        todo_data = TodoCreateModel(
            title='New Todo',
            description='This is a new todo',
            completed=False,
            user_id=1
        )
        result = await todo_service.create_todo(todo_data, session=AsyncSession)
        self.assertEqual(result.title, 'New Todo')
        self.assertEqual(result.description, 'This is a new todo')
        self.assertEqual(result.completed, False)
        self.assertEqual(result.user_id, 1)

    @patch('services.todos_service.TodoService.get_todo')
    async def test_update_todo(self, mock_get_todo):
        # Mock the get_todo function
        mock_get_todo.return_value = TodoModel(
            id=1,
            title='Existing Todo',
            description='This is an existing todo',
            completed=False,
            user_id=1
        )

        # Update an existing todo
        todo_service = TodoService()
        todo_data = TodoUpdateModel(
            title='Updated Todo',
            description='This is an updated todo',
            completed=True
        )
        result = await todo_service.update_todo(1, todo_data, session=AsyncSession)
        self.assertEqual(result.title, 'Updated Todo')
        self.assertEqual(result.description, 'This is an updated todo')
        self.assertEqual(result.completed, True)
        self.assertEqual(result.user_id, 1)

    @patch('services.todos_service.TodoService.get_todo')
    async def test_delete_todo(self, mock_get_todo):
        # Mock the get_todo function
        mock_get_todo.return_value = TodoModel(
            id=1,
            title='Existing Todo',
            description='This is an existing todo',
            completed=False,
            user_id=1
        )

        # Delete an existing todo
        todo_service = TodoService()
        result = await todo_service.delete_todo(1, session=AsyncSession)
        self.assertIsNone(result)

    @patch('services.todos_service.TodoService.get_todo')
    async def test_get_todo_by_id(self, mock_get_todo):
        # Mock the get_todo function
        mock_get_todo.return_value = TodoModel(
            id=1,
            title='Existing Todo',
            description='This is an existing todo',
            completed=False,
            user_id=1
        )

        # Get an existing todo by ID
        todo_service = TodoService()
        result = await todo_service.get_todo_by_id(1, session=AsyncSession)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.title, 'Existing Todo')
        self.assertEqual(result.description, 'This is an existing todo')
        self.assertEqual(result.completed, False)
        self.assertEqual(result.user_id, 1)

if __name__ == '__main__':
    unittest.main()

