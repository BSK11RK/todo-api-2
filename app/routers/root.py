from fastapi import APIRouter


router = APIRouter(tags=["Root"])


# ROOT
@router.get("/")
def root():
    return {"message": "ToDo API"}