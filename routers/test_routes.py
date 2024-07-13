import unittest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from routers.todo_routes import router
from fastapi import FastAPI
import json

app = FastAPI()
app.include_router(router)


class TestTodoRoutes(unittest.TestCase):
    app = FastAPI()
    app.include_router(router)

    def setUp(self):
        self.client = TestClient(app)
        self.todo_data = {'title': 'Buy groceries', 'description': 'Buy milk and eggs'}

    # Happy path tests
    @patch('routers.todo_routes.todo_service.create_todo', new_callable=AsyncMock)
    async def test_create_todo(self, mock_create_todo):
        mock_create_todo.return_value = json.dumps({'id': 1, 'title': 'Buy groceries', 'description': 'Buy milk and eggs'})
        response = await self.client.post('/todos', json=self.todo_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'id': 1, 'title': 'Buy groceries', 'description': 'Buy milk and eggs'})
        mock_create_todo.assert_called_once_with(json.dumps({'title': 'Buy groceries', 'description': 'Buy milk and eggs'}), session=AsyncMock())

        # Additional test: Verify that the created todo has the correct title and description
        created_todo = response.json()
        self.assertEqual(created_todo['title'], self.todo_data['title'])
        self.assertEqual(created_todo['description'], self.todo_data['description'])

    @patch('routers.todo_routes.todo_service.get_todo', new_callable=AsyncMock)
    async def test_get_todo(self, mock_get_todo):
        mock_get_todo.return_value = json.dumps({'id': 1, 'title': 'Buy groceries', 'description': 'Buy milk and eggs'})
        response = await self.client.get('/todos/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': 1, 'title': 'Buy groceries', 'description': 'Buy milk and eggs'})
        mock_get_todo.assert_called_once_with(1, session=AsyncMock())

        # Additional test: Verify that the retrieved todo has the correct title and description
        retrieved_todo = response.json()
        self.assertEqual(retrieved_todo['title'], 'Buy groceries')
        self.assertEqual(retrieved_todo['description'], 'Buy milk and eggs')

    @patch('routers.todo_routes.todo_service.update_todo', new_callable=AsyncMock)
    async def test_update_todo(self, mock_update_todo):
        mock_update_todo.return_value = json.dumps({'id': 1, 'title': 'Buy groceries', 'description': 'Buy milk and eggs'})
        response = await self.client.put('/todos/1', json=self.todo_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': 1, 'title': 'Buy groceries', 'description': 'Buy milk and eggs'})
        mock_update_todo.assert_called_once_with(1, json.dumps({'title': 'Buy groceries', 'description': 'Buy milk and eggs'}), session=AsyncMock())

        # Additional test: Verify that the updated todo has the correct title and description
        updated_todo = response.json()
        self.assertEqual(updated_todo['title'], self.todo_data['title'])
        self.assertEqual(updated_todo['description'], self.todo_data['description'])

    @patch('routers.todo_routes.todo_service.delete_todo', new_callable=AsyncMock)
    async def test_delete_todo(self, mock_delete_todo):
        mock_delete_todo.return_value = None
        response = await self.client.delete('/todos/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Todo deleted'})
        mock_delete_todo.assert_called_once_with(1, session=AsyncMock())

    @patch('routers.todo_routes.todo_service.get_todos', new_callable=AsyncMock)
    async def test_get_todos(self, mock_get_todos):
        mock_get_todos.return_value = [
            json.dumps({'id': 1, 'title': 'Buy groceries', 'description': 'Buy milk and eggs'}),
            json.dumps({'id': 2, 'title': 'Clean the house', 'description': 'Vacuum and mop the floors'})
        ]
        response = await self.client.get('/todos')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'id': 1, 'title': 'Buy groceries', 'description': 'Buy milk and eggs'},
            {'id': 2, 'title': 'Clean the house', 'description': 'Vacuum and mop the floors'}
        ])
        mock_get_todos.assert_called_once_with(session=AsyncMock())

        # Additional test: Verify that the number of retrieved todos is correct
        todos = response.json()
        self.assertEqual(len(todos), 2)

    # Non-happy path tests
    @patch('routers.todo_routes.todo_service.create_todo', new_callable=AsyncMock)
    async def test_create_todo_duplicate(self, mock_create_todo):
        mock_create_todo.side_effect = Exception("Todo already exists")
        response = await self.client.post('/todos', json=self.todo_data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Todo already exists"})

    @patch('routers.todo_routes.todo_service.get_todo', new_callable=AsyncMock)
    async def test_get_todo_not_found(self, mock_get_todo):
        mock_get_todo.side_effect = Exception("Todo not found")
        response = await self.client.get('/todos/999')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Todo not found"})

    @patch('routers.todo_routes.todo_service.update_todo', new_callable=AsyncMock)
    async def test_update_todo_not_found(self, mock_update_todo):
        mock_update_todo.side_effect = Exception("Todo not found")
        response = await self.client.put('/todos/999', json=self.todo_data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Todo not found"})

    @patch('routers.todo_routes.todo_service.delete_todo', new_callable=AsyncMock)
    async def test_delete_todo_not_found(self, mock_delete_todo):
        mock_delete_todo.side_effect = Exception("Todo not found")
        response = await self.client.delete('/todos/999')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Todo not found"})


if __name__ == '__main__':
    unittest.main()
            self.assertEqual(len(todos), 2)

        # Non-happy path tests
        @patch('routers.todo_routes.todo_service.create_todo', new_callable=AsyncMock)
        async def test_create_todo_duplicate(self, mock_create_todo):
            mock_create_todo.side_effect = Exception("Todo already exists")
            response = await self.client.post('/todos', json=self.todo_data)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json(), {"detail": "Todo already exists"})

        @patch('routers.todo_routes.todo_service.get_todo', new_callable=AsyncMock)
        async def test_get_todo_not_found(self, mock_get_todo):
            mock_get_todo.side_effect = Exception("Todo not found")
            response = await self.client.get('/todos/999')
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json(), {"detail": "Todo not found"})

        @patch('routers.todo_routes.todo_service.update_todo', new_callable=AsyncMock)
        async def test_update_todo_not_found(self, mock_update_todo):
            mock_update_todo.side_effect = Exception("Todo not found")
            response = await self.client.put('/todos/999', json=self.todo_data)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json(), {"detail": "Todo not found"})

        @patch('routers.todo_routes.todo_service.delete_todo', new_callable=AsyncMock)
        async def test_delete_todo_not_found(self, mock_delete_todo):
            mock_delete_todo.side_effect = Exception("Todo not found")
            response = await self.client.delete('/todos/999')
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json(), {"detail": "Todo not found"})


    if __name__ == '__main__':
        unittest.main()
