from typing import Type

from transformers import (
    AutoModel,
    AutoTokenizer,
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

    def is_cached(self) -> bool:
        """
        Check whether the model is cached, in which case a response can be generated, or if it needs to be downloaded

        :return:
        """
        try:
            AutoModel.from_pretrained(self.model_name, local_files_only=True)
            AutoTokenizer.from_pretrained(self.model_name, local_files_only=True)
        except (OSError, AttributeError):
            return False
        return True


class TranslatorFactory:
    model_class = MarianMTModel
    tokenizer_class = MarianTokenizer

    @classmethod
    def translator_factory(
        cls, input_lang: LanguageCode, output_lang: LanguageCode
    ) -> Translator:
        return Translator(cls.model_class, cls.tokenizer_class, input_lang, output_lang)
