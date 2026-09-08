from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.todo import Todo
from app.models.user import User
from app.schemas.todo import (
    TodoCreate, 
    TodoUpdate, 
    TodoPatch, 
    TodoResponse,
    TodoListResponse
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
    query = db.query(Todo).filter(
        Todo.user_id == current_user.id
    )
    
    # 検索
    if search is not None:
        search_pattern = f"%{search}%"
        
        query = query.filter(
            or_(
                Todo.title.ilike(search_pattern),
                Todo.description.ilike(search_pattern)
            )
        )
    
    # 完了状態で絞り込む
    if completed is not None:
        query = query.filter(
            Todo.completed == completed
        )
        
    # 並び替え
    if sort == "created_at":
        sort_column = Todo.created_at
    else:
        sort_column = Todo.updated_at
        
    # 昇順・降順
    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
        
    # 全件数を取得
    total = query.count()
        
    # ページ番号からoffsetを計算
    offset = (page - 1) * limit
    
    # 指定された件数だけ取得
    todos = query.offset(offset).limit(limit).all()
    
    # 総ページ数を計算
    total_pages = (total + limit - 1) // limit
    
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
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todo


# POST
@router.post("", response_model=TodoResponse, status_code=201)
def create_todo(
    todo_data: TodoCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = Todo(
        title=todo_data.title,
        description= todo_data.description,
        completed=todo_data.completed,
        user_id=current_user.id
    )
    
    db.add(todo)
    db.commit()
    db.refresh(todo)
    
    return todo


# PUT
@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.completed = todo_data.completed
    
    db.commit()
    db.refresh(todo)
    
    return todo


# PATCH
@router.patch("/{todo_id}", response_model=TodoResponse)
def patch_todo(
    todo_id: int,
    todo_data: TodoPatch,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo_data.title is not None:
        todo.title = todo_data.title
        
    if todo_data.description is not None:
        todo.description = todo_data.description
        
    if todo_data.completed is not None:
        todo.completed = todo_data.completed
        
    db.commit()
    db.refresh(todo)
    
    return todo


# DELETE
@router.delete("/{todo_id}", response_model=TodoResponse)
def delete_todo(
    todo_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    
    return todo