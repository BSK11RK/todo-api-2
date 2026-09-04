from fastapi import FastAPI

from app.database import Base, engine
from app.models import todo, user
from app.routers import todos, auth


# テーブルを作成
Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)


# ROOT
@app.get("/")
def root():
    return {"message": "Hello FastAPI"}