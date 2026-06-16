import uuid
from datetime import datetime, timezone
from uuid import UUID

from starlette.responses import JSONResponse

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from schemas import TodoCreate, TodoUpdate, TodoRead

app = FastAPI()

# Условная база данных
TODOS: list[TodoRead] = []

# Схема либо моделька Pydantic
class Item(BaseModel):
    name: str
    description: str
    price: float
    is_active: bool

@app.get("/") # Request Get по пути /
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.post("/items")
def create_item(item: Item):
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}

@app.post(
    "/todos",
    status_code=201,
    summary="Создание задачи",
    description="Базовое создание задачи без базы данных",
    response_model=TodoRead
) # Для создания ToDo
def create_todo(
        new_todo: TodoCreate
):
    todo = TodoRead(
            id=uuid.uuid4(),
            name=new_todo.name,
            description=new_todo.description,
            deadline=new_todo.deadline,
            completed=new_todo.completed
        )
    TODOS.append(
        todo
    )
    return todo

@app.put(
    "/todos/{todo_id}",
    summary="Обновление задачи",
    status_code=204
) # Для изменения существующего ToDo
def update_todo(
        todo_id: UUID,
        updated_todo: TodoUpdate
):
    for index, todo in enumerate(TODOS):
        if todo.id == todo_id:
            TODOS[index] = TodoRead(
                id=todo_id,
                name=updated_todo.name,
                description=updated_todo.description,
                deadline=updated_todo.deadline,
                completed=updated_todo.completed
            )
            return None
    return JSONResponse(
        status_code=404,
        content={
            "message": "ToDo Not Found"
        }
    )


@app.delete("/todos/{todo_id}") # Для удаления конкретного ToDo
def delete_item(
        todo_id: UUID
):
    for index, todo in enumerate(TODOS):
        if todo.id == todo_id:
            TODOS.pop(index)
            return None
    return JSONResponse(
        status_code=404,
        content={
            "message": "ToDo Not Found"
        }
    )
@app.get("/todos/{todo_id}") # Для получения конкретного ToDo
def read_item(todo_id: UUID):
    for index, todo in enumerate(TODOS):
        if todo.id == todo_id:
            return todo
    raise HTTPException(
        status_code=404,
        detail={
            "message": "Todo Not Found"
        }
    )


@app.get("/todos") # Для получения всех ToDo
def list_todos(
        q: str | None = None,
        is_completed: bool | None = None,
        deadline_start: datetime | None = None,
        deadline_end: datetime | None = None,
):
    todos = TODOS

    if q is not None:
        todos = list(filter(lambda todo: q in todo.name, todos))

    if is_completed is not None:
        todos = list(filter(lambda todo: todo.completed == is_completed, todos))

    if deadline_start is not None:
        deadline_start = deadline_start.replace(tzinfo=timezone.utc)
        todos = list(filter(lambda todo: todo.deadline >= deadline_start, todos))

    if deadline_end is not None:
        deadline_end = deadline_end.replace(tzinfo=timezone.utc)
        todos = list(filter(lambda todo: todo.deadline <= deadline_end, todos))

    return todos