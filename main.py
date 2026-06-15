from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

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

