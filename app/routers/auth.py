from fastapi import APIRouter, Depends, HTTPException
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse


router = APIRouter(prefix="/auth", tags=["Auth"])


password_hash = PasswordHash.recommended()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    exsting_user = db.query(User).filter(
        User.email == user_data.email
    ).first()
    
    if exsting_user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = password_hash.hash(user_data.password)
    
    user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user