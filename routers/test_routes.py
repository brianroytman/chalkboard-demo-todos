import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from fastapi import status
from main import app
from schemas import TodoModel, TodoCreateModel
from services.todos_service import TodoService

class TestTodoRoutes(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch.object(TodoService, 'create_todo', return_value=TodoModel(
        id=1,
        title="Test Todo",
        description="This is a test todo",
        is_completed=False,
        date_created="2024-07-14T12:00:00Z",
        date_updated="2024-07-14T12:00:00Z",
        user_id=1
    ))
    def test_create_todo(self, mock_create_todo):
        mock_todo_data = TodoCreateModel(
            title="Test Todo",
            description="This is a test todo",
            is_completed=False,
            user_id=1
        )
        
        response = self.client.post("/todos", json={
            "title": "Test Todo",
            "description": "This is a test todo",
            "is_completed": False,
            "user_id": 1    
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Test Todo")
        mock_create_todo.assert_called_once_with(mock_todo_data, unittest.mock.ANY)
    
    @patch.object(TodoService, 'create_todo', side_effect=Exception("User not found"))
    def test_create_todo_user_not_found(self, mock_create_todo):
        response = self.client.post("/todos", json={
            "title": "Test Todo",
            "description": "This is a test todo",
            "is_completed": False,
            "user_id": 1
        })

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("User not found", response.json()["detail"])
        mock_create_todo.assert_called_once()

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
    
    @patch.object(TodoService, 'get_user_todos', return_value=[
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
    def test_get_user_todos(self, mock_get_user_todos):
        response = self.client.get("/users/1/todos")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        mock_get_user_todos.assert_called_once_with(1, unittest.mock.ANY)

    @patch.object(TodoService, 'get_user_todos', return_value=[])
    def test_get_user_todos_empty(self, mock_get_user_todos):
        response = self.client.get("/users/1/todos")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
        mock_get_user_todos.assert_called_once_with(1, unittest.mock.ANY)
    
    @patch.object(TodoService, 'get_user_todos', side_effect=Exception("User not found"))
    def test_get_user_todos_user_not_found(self, mock_get_user_todos):
        response = self.client.get("/users/999/todos")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("User not found", response.json()["detail"])
        mock_get_user_todos.assert_called_once_with(999, unittest.mock.ANY)

if __name__ == '__main__':
    unittest.main()
