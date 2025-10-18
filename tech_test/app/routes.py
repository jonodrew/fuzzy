from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/")
def index():
    return {"message": "Hello world"}
