from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


# DBエンジン
engine = create_engine(settings.database_url)


# DBセッション
SessionLocal = sessionmaker(
    bind=engine, 
    autocommit=False, 
    autoflush=False
)


# モデルの親クラス
class Base(DeclarativeBase):
    pass


# FastAPIからDBセッションを取得するための関数
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()