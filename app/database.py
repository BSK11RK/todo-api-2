from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# プロジェクトのルートディレクトリ
BASE_DIR = Path(__file__).resolve().parent.parent

# dataフォルダ
DATA_DIR = BASE_DIR / "data"

# dataフォルダがなければ作成
DATA_DIR.mkdir(exist_ok=True)

# SQLiteデータベースのパス
DATABASE_URL = f"sqlite:///{DATA_DIR / 'todos.db'}"


# DBエンジン
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# DBセッション
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


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