from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID


# Схема для данных ToDo
class TodoBase(BaseModel):
    name: str = Field(min_length=3, max_length=255) # 3-255 символов
    description: str | None = Field(max_length=1024) # 1024 макс символов
    completed: bool = Field(default=False) # По умолчанию False
    deadline: datetime

# Схема для создания ToDo
class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: UUID