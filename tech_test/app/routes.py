from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse

from tech_test.services.languages import LanguageCode
from tech_test.services.translator import TranslatorFactory

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
def translate(data: TranslationInput):
    translator = TranslatorFactory.translator_factory(
        data.input_language, data.output_language
    )
    if not translator.is_cached():
        return JSONResponse(
            status_code=202,
            content={
                "message": "We're just grabbing that model for you. Hold tight, and ping us again in 300 seconds"
            },
        )
    if not translator.is_valid():
        raise HTTPException(
            status_code=422,
            detail={"message": "That language pair doesn't exist right now"},
        )
    return data.model_dump()
