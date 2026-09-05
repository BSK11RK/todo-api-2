from fastapi import FastAPI

from app.database import Base, engine
from app.models import todo, user
from app.routers import auth, root, todos, users


# テーブルを作成
Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(root.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)