from typing import Type

from transformers import (
    MarianMTModel,
    MarianTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
)

from tech_test.services.languages import LanguageCode


class Translator:
    def __init__(
        self,
        model_class: Type[PreTrainedModel],
        tokenizer_class: Type[PreTrainedTokenizer],
        input_lang: LanguageCode,
        output_lang: LanguageCode,
    ) -> None:
        self.model_name = f"Helsinki-NLP/opus-mt-{input_lang}-{output_lang}"
        self.model_class = model_class
        self.tokenizer_class = tokenizer_class


class TranslatorFactory:
    model_class = MarianMTModel
    tokenizer_class = MarianTokenizer

    @classmethod
    def translator_factory(
        cls, input_lang: LanguageCode, output_lang: LanguageCode
    ) -> Translator:
        return Translator(cls.model_class, cls.tokenizer_class, input_lang, output_lang)
