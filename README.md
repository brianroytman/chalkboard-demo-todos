# Chalkboard Demo Todos Microservice

This repository contains the code for the chalkboard_demo_todos project, which consists of the Todo Service responsible for managing todo-related operations.

## Technologies Used

The following technologies were used in this project:

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- OpenAPI/Swagger

## Directory Structure

The directory structure of this project is as follows:

### Todo Service

- `repositories/todo_repository.py`: Implements database operations using SQLAlchemy for todos.
- `routers/todo_routes.py`: Defines API routes and endpoints using FastAPI, depending on services for request handling.
- `services/todo_service.py`: Implements business logic and coordinates with repositories for todos.
- `create_db.py`: Script for creating the PostgreSQL database required for the todos service.
- `database.py`: Manages the PostgreSQL database connection.
- `main.py`: Initializes the FastAPI application for todos.
- `models.py`: Defines SQLAlchemy models for todos.
- `schemas.py`: Pydantic schemas for input/output validation related to todos.

## Setup Instructions

To set up and run this project locally without Docker, follow these instructions:

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd chalkboard_demo_todos
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the database:
    - Ensure PostgreSQL is running locally or configure connection settings in `.env`.
    - Run the following command to create the database:
    ```sh
    py create_db.py
    ```

4. Start the Todo Service:
    - Run the following command to start the Todo Service:
    ```sh
    uvicorn main:app --reload --port 8000
    ```

5. Access the Todo Service API documentation:
    - Open your web browser and go to `http://localhost:8000/docs` to access the Swagger UI documentation for the Todo Service API.

## cURL Request Examples for Todos
- GET /todos/
```sh
curl -X 'GET' \
    'http://127.0.0.1:8000/todos' \
    -H 'accept: application/json'
```

- POST /todos/
```sh
curl -X 'POST' \
    'http://127.0.0.1:8000/todos' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "title": "Buy groceries",
    "description": "Go to the supermarket and buy groceries",
    "is_completed": false,
    "user_id": 1
}'
```

- GET /todos/{todo_id}
```sh
curl -X 'GET' \
    'http://127.0.0.1:8000/todos/1' \
    -H 'accept: application/json'
```

- PUT /todos/{todo_id}/
```sh
curl -X 'PUT' \
    'http://127.0.0.1:8000/todos/1' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "title": "UPDATE Buy groceries",
    "description": "Go to the supermarket and buy groceries",
    "is_completed": true,
    "user_id": 1
}'
```

- DELETE /todos/{todo_id}/
```sh
curl -X 'DELETE' \
    'http://127.0.0.1:8000/todos/6' \
    -H 'accept: */*'
```

## Running Tests for Todos

To run the tests for this project, use the following commands:

```sh
py -m unittest -v routers/test_routes.py
py -m unittest -v services/test_services.py
py -m unittest -v repositories/test_repository.py
```