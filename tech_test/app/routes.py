from fastapi import APIRouter
from pydantic import BaseModel

from tech_test.services.languages import LanguageCode

api_router = APIRouter()


@api_router.get("/")
def index():
    return {"message": "Hello world"}


class TranslationInput(BaseModel):
    input_language: LanguageCode = "en"
    output_language: LanguageCode
    input_text: str


class TranslationOutput(TranslationInput):
    output_text: str = "Coming soon!"


@api_router.post("/translate", response_model=TranslationOutput)
def translate(data: TranslationInput) -> dict:
    return data.model_dump()
