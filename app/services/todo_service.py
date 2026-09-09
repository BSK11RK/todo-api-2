from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.todo import Todo


# GET
def get_todos(
    db: Session,
    user_id: int,
    search: str | None,
    completed: bool | None,
    sort: str,
    order: str,
    page: int,
    limit: int
):
    # ユーザーのTodo一覧を取得
    query = db.query(Todo).filter(
        Todo.user_id == user_id
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
        
    # 完了状態
    if completed is not None:
        query = query.filter(
            Todo.completed == completed
        )
        
    # ソート対象
    if sort == "created_at":
        sort_column = Todo.created_at
    else:
        sort_column = Todo.updated_at
        
    # ソート順
    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
        
    # 全件数
    total = query.count()
    
    # ページネーション
    offset = (page - 1) * limit
    
    todos = query.offset(offset).limit(limit).all()
    
    total_pages = (total + limit - 1) // limit
    
    return todos, total, total_pages


# GET_ID
def get_todo(
    db: Session,
    user_id: int,
    todo_id: int
):
    return db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == user_id
    ).first()
    
    
# POST
def create_todo(
    db: Session,
    user_id: int,
    title: str,
    description: str,
    completed: bool
):
    todo = Todo(
        title=title,
        description=description,
        completed=completed,
        user_id=user_id
    )
    
    db.add(todo)
    db.commit()
    db.refresh(todo)
    
    return todo


# PUT
def update_todo(
    db: Session,
    todo: Todo,
    title: str,
    description: str,
    completed: bool
):
    todo.title = title
    todo.description = description
    todo.completed = completed
    
    db.commit()
    db.refresh(todo)
    
    return todo


# PATCH
def patch_todo(
    db: Session,
    todo: Todo,
    title: str | None,
    description: str | None,
    completed: bool | None
):
    if title is not None:
        todo.title = title
        
    if description is not None:
        todo.description = description
        
    if completed is not None:
        todo.completed = completed
        
    db.commit()
    db.refresh(todo)
    
    return todo


# DELETE
def delete_todo(db: Session, todo: Todo):
    db.delete(todo)
    db.commit()
    
    return todo