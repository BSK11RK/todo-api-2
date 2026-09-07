from fastapi import FastAPI
from app.routers import auth, root, todos, users


app = FastAPI()

app.include_router(root.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)