from fastapi import FastAPI

from app.database import Base, engine
from app.models.todo import Todo
from app.routers import todos


# テーブルを作成
Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(todos.router)


# ROOT
@app.get("/")
def root():
    return {"message": "Hello FastAPI"}