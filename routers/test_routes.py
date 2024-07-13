import unittest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from fastapi import status, FastAPI
from routers.todo_routes import router
from schemas import TodoModel, TodoCreateModel
from exceptions.user_not_found_exception import UserNotFoundException

app = FastAPI()
app.include_router(router)

class TestTodoRoutes(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch('routers.todo_routes.todos_service.create_todo', new_callable=AsyncMock)
    async def test_create_todo(self, mock_create_todo):
        mock_todo_create = TodoCreateModel(
            title='Test Todo',
            description='This is a test todo',
            is_completed=False,
            user_id=1
        )
        mock_create_todo.return_value = TodoModel(**mock_todo_create.dict(), id=1)

        response = await self.client.post('/todos', json=mock_todo_create.dict())
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), mock_todo_create.dict())
        mock_create_todo.assert_called_once_with(mock_todo_create, session=AsyncMock())

    @patch('routers.todo_routes.todos_service.create_todo', new_callable=AsyncMock)
    async def test_create_todo_exception(self, mock_create_todo):
        mock_create_todo.side_effect = UserNotFoundException("User not found")

        response = await self.client.post('/todos', json={'title': 'Test Todo'})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "User not found"})

    @patch('routers.todo_routes.todos_service.get_todo', new_callable=AsyncMock)
    async def test_get_todo(self, mock_get_todo):
        mock_todo = TodoModel(id=1, title='Test Todo', description='This is a test todo', is_completed=False, user_id=1)
        mock_get_todo.return_value = mock_todo

        response = await self.client.get('/todos/1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), mock_todo.dict())
        mock_get_todo.assert_called_once_with(1, session=AsyncMock())

    @patch('routers.todo_routes.todos_service.get_todo', new_callable=AsyncMock)
    async def test_get_todo_not_found(self, mock_get_todo):
        mock_get_todo.side_effect = UserNotFoundException("Todo not found")

        response = await self.client.get('/todos/999')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Todo not found"})

    @patch('routers.todo_routes.todos_service.get_todos', new_callable=AsyncMock)
    async def test_get_todos(self, mock_get_todos):
        mock_todos = [
            TodoModel(id=1, title='Test Todo 1', description='This is test todo 1', is_completed=False, user_id=1),
            TodoModel(id=2, title='Test Todo 2', description='This is test todo 2', is_completed=True, user_id=1)
        ]
        mock_get_todos.return_value = mock_todos

        response = await self.client.get('/todos')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [todo.dict() for todo in mock_todos])
        mock_get_todos.assert_called_once_with(session=AsyncMock())

    @patch('routers.todo_routes.todos_service.update_todo', new_callable=AsyncMock)
    async def test_update_todo(self, mock_update_todo):
        updated_data = {'title': 'Updated Test Todo', 'description': 'Updated description', 'is_completed': True}
        mock_update_todo.return_value = TodoModel(id=1, user_id=1, **updated_data)

        response = await self.client.put('/todos/1', json=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': 1, 'user_id': 1, **updated_data})
        mock_update_todo.assert_called_once_with(1, updated_data, session=AsyncMock())

    @patch('routers.todo_routes.todos_service.update_todo', new_callable=AsyncMock)
    async def test_update_todo_not_found(self, mock_update_todo):
        mock_update_todo.side_effect = UserNotFoundException("Todo not found")

        response = await self.client.put('/todos/999', json={'title': 'Updated Test Todo'})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Todo not found"})

    @patch('routers.todo_routes.todos_service.delete_todo', new_callable=AsyncMock)
    async def test_delete_todo(self, mock_delete_todo):
        mock_delete_todo.return_value = None

        response = await self.client.delete('/todos/1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Todo deleted"})
        mock_delete_todo.assert_called_once_with(1, session=AsyncMock())

    @patch('routers.todo_routes.todos_service.delete_todo', new_callable=AsyncMock)
    async def test_delete_todo_not_found(self, mock_delete_todo):
        mock_delete_todo.side_effect = UserNotFoundException("Todo not found")

        response = await self.client.delete('/todos/999')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Todo not found"})

    @patch('routers.todo_routes.todos_service.get_user_todos', new_callable=AsyncMock)
    async def test_get_user_todos(self, mock_get_user_todos):
        mock_user_id = 1
        mock_todos = [
            TodoModel(id=1, title='Test Todo 1', description='This is test todo 1', is_completed=False, user_id=mock_user_id),
            TodoModel(id=2, title='Test Todo 2', description='This is test todo 2', is_completed=True, user_id=mock_user_id)
        ]
        mock_get_user_todos.return_value = mock_todos

        response = await self.client.get(f'/todos/user/{mock_user_id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [todo.dict() for todo in mock_todos])
        mock_get_user_todos.assert_called_once_with(mock_user_id, session=AsyncMock())

if __name__ == '__main__':
    unittest.main()
