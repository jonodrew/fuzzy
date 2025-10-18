from fastapi import APIRouter
from pydantic import BaseModel

api_router = APIRouter()


@api_router.get("/")
def index():
    return {"message": "Hello world"}


class TranslationInput(BaseModel):
    input_language: str = "en"
    output_language: str
    input_text: str


class TranslationOutput(TranslationInput):
    output_text: str = "Coming soon!"


@api_router.post("/translate", response_model=TranslationOutput)
def translate(data: TranslationInput) -> dict:
    return data.model_dump()
