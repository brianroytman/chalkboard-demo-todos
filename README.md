# Chalkboard Demo Todos Microservice

This repository contains the code for the chalkboard_demo_todos project, which consists of the Todos microservice responsible for managing todo-related operations tied to users via an interconnected Users microservice.
[Users microservice](https://github.com/brianroytman/chalkboard-demo-users)

## Table of Contents

- [Technologies Used](#technologies-used)
- [Considerations](#considerations)
  - [Async Operations](#async-operations)
  - [CQRS Pattern](#cqrs-pattern)
  - [Repository Pattern](#repository-pattern)
- [Project Structure](#project-structure)
  - [Todos Service](#todos-service)
- [Setup Instructions](#setup-instructions)
  - [Run Local](#run-local)
  - [Run via Docker](#run-via-docker)
- [cURL Request Examples for Todos](#curl-request-examples-for-todos)
- [Live Demo](#live-demo)
- [Running Tests for Todos](#running-tests-for-todos)

## Technologies Used

The following technologies were used in this project:

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- OpenAPI/Swagger

## Considerations

### Async Operations
- **Improved Performance:** Non-blocking operations allow handling more concurrent requests efficiently.
- **Scalability:** Utilizes server resources better by overlapping tasks and improving CPU and I/O utilization.
- **Responsive Applications:** Ensures applications remain responsive to requests, providing faster responses to clients.

### CQRS Pattern

1. **CQRS Pattern Overview**
   - Separates the responsibility for handling read and write operations into different components.
   - Optimizes query performance and scalability by tailoring data models and access patterns for read and write operations separately.

2. **Key Components**
   - **Command Side:** Handles write operations (e.g., create, update, delete), enforcing business rules and updating the data store.
   - **Query Side:** Handles read operations, optimized for querying and presenting data without affecting write operations.

3. **Implementation Alignment**
   - **Command Handler (Write)**: Receives commands from the client, validates inputs, processes business logic, and updates the data store.
   - **Query Handler (Read)**: Handles queries for retrieving data, optimizes data access patterns, and prepares data for presentation.

###### CQRS Pattern Examples: Create Todo and Get All Todos by User
```mermaid
   sequenceDiagram
    participant ui as UI
    participant cr as Command Route
    participant ch as Command Handler
    participant us as Users Service
    participant qr as Query Route
    participant qh as Query Handler
    participant td as Todos Table

    ui ->> cr: POST /todos routes.create_todo
    cr ->> ch: commands.create_todo
    ch ->> us: Check if user exists
    us -->> ch: True
    ch ->> td: Insert new Todo record into DB
    td -->> ch: Return operation success
    ch -->> cr: Return response to route
    cr -->> ui: Return response to UI

    ui ->> qr: GET /todos/user/{user_id} routes.get_todos
    qr ->> qh: queries.get_todos
    qh ->> us: Check if user exists
    us -->> qh: True
    qh ->> td: Select all Todos records from DB
    td -->> qh: Return Todos records
    qh -->> qr: Return Todos to route
    qr -->> ui: Return Todos response
```


### Repository Pattern

1. **Repository Pattern Overview**
   - Abstracts data access logic, separating it from the application's business logic.
   - Provides centralized access to data, hiding details of data storage, retrieval, and manipulation.

2. **Key Components**
   - **Data Access Abstraction:** Encapsulates logic for CRUD operations, shields the business logic from database specifics.
   - **Separation of Concerns:** Promotes modular and maintainable code by isolating changes in data storage technology or schema.

3. **Implementation Alignment**
   - **Router (Controller) Layer:** Handles HTTP requests, validates inputs, delegates processing to the service layer.
   - **Service (Business Logic) Layer:** Implements application-specific rules, coordinates with repositories for data operations.
   - **Repository (Data Access) Layer:** Manages database interactions, offers a unified interface for data access operations.

###### Repository Pattern: Create Todo Example
```mermaid
sequenceDiagram
    participant ui as UI
    participant tr as Todos Route
    participant ts as Todos Service
    participant trp as Todos Repository
    participant us as Users Service
    participant ud as Users Table
    participant td as Todos Table

    ui ->> tr: POST /todos routes.create_todo
    tr ->> ts: services.create_todo
    ts ->> us: HTTP service call: Check User Exists
    us ->> ud: Get User by UserId
    ud ->> us: User Found
    us ->> ts: True
    ts ->> trp: repositories.add
    trp ->> td: Write new Todo record to DB
    td -->> trp: Operation success response
    trp -->> ts: Return operation success
    ts -->> tr: Return operation success
    tr -->> ui: Return operation success
```


4. **Advantages**
   - **Testability:** Enables independent testing of business logic using mock repositories.
   - **Flexibility:** Minimizes impact of database technology or schema changes by confining them to the repository layer.
   - **Centralized Data Access:** Promotes code reuse, ensures consistent data access patterns across the application.


## Project Structure

The directory structure of this project is as follows:

### Todos Service

```
chalkboard_demo_todos/
├── Dockerfile
├── requirements.txt
├── docker-compose.yml
├── main.py
├── create_db.py
├── database.py
├── dependencies.py
├── models.py
├── schemas.py
├── services/
│ ├── todo_service.py
│ └── test_services.py
├── repositories/
│ ├── todo_repository.py
│ └── test_repository.py
├── routers/
│ ├── todo_routes.py
│ └── test_routes.py
├── handlers/
│ ├── command_handler.py
│ └── query_handler.py
├── commands.py
├── queries.py
├── exceptions/
│ └── user_not_found_exception.py
```

- `repositories/todo_repository.py`: Implements database operations using SQLAlchemy for todos.
- `routers/todo_routes.py`: Defines API routes and endpoints using FastAPI, depending on services for request handling.
- `services/todo_service.py`: Implements business logic and coordinates with repositories for todos.
- `commands.py`: Contains SQLAlchemy model for commands related to todos - creating new todos.
- `queries.py`: Contains SQLAlchemy model for queries related to todos - retrieving todos by user ID.
- `handlers/command_handler.py`: Handles command execution and business logic for todos, coordinating with services and repositories.
- `handlers/query_handler.py`: Manages query handling and data retrieval for todos, interfacing with the database and services.
- `create_db.py`: Script for creating the PostgreSQL database required for the todos service.
- `database.py`: Manages the PostgreSQL database connection.
- `main.py`: Initializes the FastAPI application for todos.
- `models.py`: Defines SQLAlchemy models for todos.
- `schemas.py`: Pydantic schemas for input/output validation related to todos.


## API Endpoints

| Action            | HTTP Method | Endpoint                          |
|-------------------|-------------|-----------------------------------|
| Create a Todo     | POST        | /todos                           |
| Read Todos        | GET         | /todos                           |
| Read a Todo by ID | GET         | /todos/{todo_id}                 |
| Update a Todo     | PUT         | /todos/{todo_id}                 |
| Delete a Todo     | DELETE      | /todos/{todo_id}                 |
| Read All Todos by UserID| GET         | /todos/user/{user_id}             |

## Setup Instructions

### Run Local

To set up and run this project locally, follow these instructions:
    - Note: In order to create and update Todos with an associated UserId, the Users service must also be running

1. Clone each repository and run in dedicated terminals:
    ```sh
    git clone https://github.com/brianroytman/chalkboard-demo-todos.git
    cd chalkboard_demo_todos
    ```
    ```sh
    git clone https://github.com/brianroytman/chalkboard-demo-users.git
    cd chalkboard_demo_users
    ```

2. Install the required dependencies for each service/ in each terminal session:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the database:
    - Ensure PostgreSQL is running locally or configure connection settings in `.env`.
    - Run the following command to create the database for each each service/in each terminal session:
    ```sh
    py create_db.py
    ```

4. Start the Todos Service:
    - Run the following commands to start the Todos service and the Users service:
    ```sh
    uvicorn main:app --reload --port 8000
    ```
    ```sh
    uvicorn main:app --reload --port 8001
    ```

5. Access the Todo Service API documentation:
    - Open your web browser and go to `http://localhost:8000` to access the Swagger UI documentation and endpoints for the Todos service API.

### Run via Docker

To set up and run this project with Docker, follow these instructions:
- Note: The Todos service docker-compose.yml file has configuration details for starting up + connecting to the Users service as well as the Todos service (for interservice call to check if user exists)
- Note: Both repos need to be cloned and live under the same root directory

1. Clone both repositories and navigate to the root directory of the Todos service:
```sh
git clone https://github.com/brianroytman/chalkboard-demo-users.git
git clone https://github.com/brianroytman/chalkboard-demo-todos.git
cd chalkboard-demo-todos
```

2. Make sure Docker is installed on your machine:

3. Run Docker Compose:
```sh
docker-compose build
docker-compose up
```

4. Access the Todos service and Users in your web browser:
    - Users service must be up and running for Todos.Create and Todos.Update endpoints to function
```sh
http://localhost:8000 (Todos)
http://localhost:8001 (Users)
```

5. Interact with Todos service endpoints via web browser

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

- GET /todos/user/{user_id}
```sh
curl -X 'GET' \
    'http://127.0.0.1:8000/todos/user/1' \
    -H 'accept: application/json'
```

## Live Demo
[Live Demo](https://www.loom.com/share/e5726e64133b42a5b1cafd9a031d7c61?sid=5776570b-9b91-496b-aaf4-9ee28a2fcc93)

## Running Tests for Todos

To run the tests for this project, use the following commands:

```sh
py -m unittest -v routers/test_routes.py
py -m unittest -v services/test_services.py
py -m unittest -v repositories/test_repository.py
```
