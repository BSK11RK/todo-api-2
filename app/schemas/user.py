# APIで受け取る・返すデータの設計
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    
    model_config = {"from_attributes": False}