from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.security import password_hash


router = APIRouter(prefix="/users", tags=["Users"])


# GET_ME
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# PATCH
@router.patch("/me", response_model=UserResponse)
def update_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # emailが送られてきた場合
    if user_data.email is not None:

        existing_user = db.query(User).filter(
                User.email == user_data.email,
                User.id != current_user.id,
            ).first()

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        current_user.email = user_data.email

    # passwordが送られてきた場合
    if user_data.password is not None:
        current_user.hashed_password = password_hash.hash(user_data.password)

    db.commit()
    db.refresh(current_user)

    return current_user


# DELETE
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.delete(current_user)
    db.commit()

    return None