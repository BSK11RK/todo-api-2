from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.todo import (
    TodoCreate, 
    TodoUpdate, 
    TodoPatch, 
    TodoResponse,
    TodoListResponse
)
from app.services.todo_service import (
    create_todo as create_todo_service,
    delete_todo as delete_todo_service,
    get_todo as get_todo_service,
    get_todos as get_todos_service,
    patch_todo as patch_todo_service,
    update_todo as update_todo_service
)


router = APIRouter(prefix="/todos", tags=["Todos"])


# GET
@router.get("", response_model=TodoListResponse)
def get_todos(
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
        description="Todoのタイトルまたは説明を検索"
    ),
    completed: bool | None = Query(
        default=None, 
        description="完全状態で絞り込む"
    ),
    # 入力できる値をこの2つに限定する
    sort: Literal["created_at", "updated_at"] = Query(
        default="created_at",
        description="並び替える項目"
    ),
    order: Literal["asc", "desc"] = Query(
        default="desc",
        description="並び順"
    ),
    page: int = Query(default=1, ge=1, description="ページ番号"),
    limit: int = Query(
        default=10, 
        ge=1, 
        le=100, 
        description="1ページあたりの件数"
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todos, total, total_pages = get_todos_service(
        db=db,
        user_id=current_user.id,
        search=search,
        completed=completed,
        sort=sort,
        order=order,
        page=page,
        limit=limit
    )
    
    return {
        "items": todos,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages
    }


# GET_ID
@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = get_todo_service(
        db=db,
        user_id=current_user.id,
        todo_id=todo_id
    )
    
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
        )
    
    return todo


# POST
@router.post(
    "", 
    response_model=TodoResponse, 
    status_code=status.HTTP_201_CREATED
)
def create_todo(
    todo_data: TodoCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_todo_service(
        db=db,
        user_id=current_user.id,
        title=todo_data.title,
        description=todo_data.description,
        completed=todo_data.completed
    )


# PUT
@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = get_todo_service(
        db=db,
        user_id=current_user.id,
        todo_id=todo_id
    )
    
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Todo not found"
        )
    
    return update_todo_service(
        db=db,
        todo=todo,
        title=todo_data.title,
        description=todo_data.description,
        completed=todo_data.completed
    )


# PATCH
@router.patch("/{todo_id}", response_model=TodoResponse)
def patch_todo(
    todo_id: int,
    todo_data: TodoPatch,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = get_todo_service(
        db=db,
        user_id=current_user.id,
        todo_id=todo_id
    )
    
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
        )
    
    return patch_todo_service(
        db=db,
        todo=todo,
        title=todo_data.title,
        description=todo_data.description,
        completed=todo_data.completed
    )


# DELETE
@router.delete("/{todo_id}", response_model=TodoResponse)
def delete_todo(
    todo_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    todo = get_todo_service(
        db=db,
        user_id=current_user.id,
        todo_id=todo_id
    )
    
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
        )
    
    return delete_todo_service(db=db, todo=todo)