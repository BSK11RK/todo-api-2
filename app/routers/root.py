from fastapi import APIRouter


router = APIRouter(prefix="/root", tags=["Root"])


# ROOT
@router.get("/")
def root():
    return {"message": "ToDo API"}