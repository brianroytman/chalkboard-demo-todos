import unittest
import httpx
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from fastapi import status
from main import app  # Import your FastAPI app
from schemas import TodoModel
from exceptions.user_not_found_exception import UserNotFoundException
from services.todos_service import TodoService
from unittest.mock import patch, AsyncMock
from fastapi import status
from handlers.query_handler import TodoQueryHandler
from handlers.command_handler import TodoCommandHandler

class TestTodoRoutes(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch.object(TodoCommandHandler, 'handle_create_todo_command', return_value=TodoModel(
        id=1,
        title="Test Todo",
        description="This is a test todo",
        is_completed=False,
        user_id=1,
        date_created="2024-07-14T12:00:00Z",
        date_updated="2024-07-14T12:00:00Z"
    ))  
    @patch.object(TodoService, 'check_user_exists', return_value=True)
    def test_create_todo_user_exists(self, mock_check_user_exists, mock_handle_create_todo_command):
        response = self.client.post("/todos", json={
            "title": "Test Todo",
            "description": "This is a test todo",
            "is_completed": False,
            "user_id": 1
        })

        # Assert HTTP status code and response content
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Test Todo")
        self.assertEqual(response.json()["description"], "This is a test todo")
        self.assertFalse(response.json()["is_completed"])

        # Ensure handle_create_todo_command was called exactly once
        mock_handle_create_todo_command.assert_called_once()

    @patch.object(TodoCommandHandler, 'handle_create_todo_command', side_effect=UserNotFoundException("User not found"))
    def test_create_todo_user_not_found(self, mock_handle_create_todo_command):
        response = self.client.post("/todos", json={
            "title": "Test Todo",
            "description": "This is a test todo",
            "is_completed": False,
            "user_id": 1
        })

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("User not found", response.json()["detail"])
        mock_handle_create_todo_command.assert_called_once()

    @patch.object(TodoService, 'get_todo', return_value=TodoModel(
        id=1,
        title="Test Todo",
        description="This is a test todo",
        is_completed=False,
        date_created="2024-07-14T12:00:00Z",
        date_updated="2024-07-14T12:00:00Z",
        user_id=1
    ))
    def test_get_todo(self, mock_get_todo):
        response = self.client.get("/todos/1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], "Test Todo")
        mock_get_todo.assert_called_once_with(1, unittest.mock.ANY)

    @patch.object(TodoService, 'get_todo', return_value=None)
    def test_get_todo_not_found(self, mock_get_todo):
        response = self.client.get("/todos/999")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("Todo not found", response.json()["detail"])
        mock_get_todo.assert_called_once_with(999, unittest.mock.ANY)

    @patch.object(TodoService, 'get_todos', return_value=[
        TodoModel(
            id=1,
            title="Test Todo",
            description="This is a test todo",
            is_completed=False,
            date_created="2024-07-14T12:00:00Z",
            date_updated="2024-07-14T12:00:00Z",
            user_id=1
        )
    ])
    def test_get_todos(self, mock_get_todos):
        response = self.client.get("/todos")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        mock_get_todos.assert_called_once_with(unittest.mock.ANY)

    @patch.object(TodoService, 'update_todo', return_value=TodoModel(
        id=1,
        title="Test Todo",
        description="This is a test todo",
        is_completed=False,
        date_created="2024-07-14T12:00:00Z",
        date_updated="2024-07-14T12:00:00Z",
        user_id=1
    ))
    def test_update_todo(self, mock_update_todo):
        response = self.client.put("/todos/1", json={
            "title": "Test Todo",
            "description": "This is a test todo",
            "is_completed": False,
            "user_id": 1
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], "Test Todo")
        mock_update_todo.assert_called_once_with(1, unittest.mock.ANY, unittest.mock.ANY)

    @patch.object(TodoService, 'update_todo', return_value=None)
    def test_update_todo_not_found(self, mock_update_todo):
        response = self.client.put("/todos/999", json={
            "title": "Test Todo",
            "description": "This is a test todo",
            "is_completed": False,
            "user_id": 1
        })

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("Todo not found", response.json()["detail"])
        mock_update_todo.assert_called_once_with(999, unittest.mock.ANY, unittest.mock.ANY)

    @patch.object(TodoService, 'delete_todo')
    def test_delete_todo(self, mock_delete_todo):
        response = self.client.delete("/todos/1")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        mock_delete_todo.assert_called_once_with(1, unittest.mock.ANY)

    @patch.object(TodoService, 'delete_todo', side_effect=Exception("Todo not found"))
    def test_delete_todo_not_found(self, mock_delete_todo):
        response = self.client.delete("/todos/999")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("Todo not found", response.json()["detail"])
        mock_delete_todo.assert_called_once_with(999, unittest.mock.ANY)
    
    @patch.object(TodoQueryHandler, 'handle_get_todos_by_user_query', new_callable=AsyncMock)
    @patch.object(TodoService, 'check_user_exists', return_value=bool)
    def test_get_user_todos(self, mock_check_user_exists, mock_handle_get_todos_by_user_query):
        mock_check_user_exists.return_value = True
        mock_handle_get_todos_by_user_query.return_value = [
            TodoModel(
                id=1,
                title="Test Todo 1",
                description="Description 1",
                is_completed=False,
                user_id=1,
                date_created="2024-07-15T12:00:00Z",  
                date_updated="2024-07-15T12:00:00Z"   
            ),
            TodoModel(
                id=2,
                title="Test Todo 2",
                description="Description 2",
                is_completed=True,
                user_id=1,
                date_created="2024-07-15T12:00:00Z", 
                date_updated="2024-07-15T12:00:00Z"  
            )
        ]

        response = self.client.get("/todos/user/1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todos = response.json()
        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[0]["title"], "Test Todo 1")
        self.assertEqual(todos[1]["description"], "Description 2")
        mock_handle_get_todos_by_user_query.assert_called_once()

if __name__ == '__main__':
    unittest.main()
