from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.todo import Todo


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