from fastapi import FastAPI
from routers import todo_routes

app = FastAPI(
    title="Chalkboard Todo FastAPI Postgres Async App - Todos Microservice",
    description="ToDo and Users Microservices using FastAPI, PostgreSQL, and SQLAlchemy Async",
    docs_url="/",
)

app.include_router(todo_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
