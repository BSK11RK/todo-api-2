# APIで受け取る・返すデータの設計
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
    
    model_config = {"from_attributes": True}