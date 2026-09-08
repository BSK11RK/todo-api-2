# APIで受け取る・返すデータの設計
from datetime import datetime
from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    description: str
    completed: bool = False
    
    
class TodoUpdate(BaseModel):
    title: str
    description: str
    completed: bool
    
    
class TodoPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    
    
class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}
    
    
class TodoListResponse(BaseModel):
    items: list[TodoResponse]
    page: int
    limit: int
    total: int
    total_pages: int