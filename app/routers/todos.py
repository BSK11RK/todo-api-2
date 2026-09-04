from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoPatch, TodoResponse


router = APIRouter(prefix="/todos", tags=["Todos"])


# GET
@router.get("", response_model=list[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    
    return todos


# GET_ID
@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(
        Todo.id == todo_id
    ).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todo


# POST
@router.post("", response_model=TodoResponse, status_code=201)
def create_todo(todo_data: TodoCreate, db: Session = Depends(get_db)):
    todo = Todo(
        title=todo_data.title,
        description= todo_data.description,
        completed=todo_data.completed
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
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(
        Todo.id == todo_id
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
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(
        Todo.id == todo_id
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
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(
        Todo.id == todo_id
    ).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    
    return todo