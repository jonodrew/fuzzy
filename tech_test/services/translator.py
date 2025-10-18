from typing import Type

from huggingface_hub import model_info
from huggingface_hub.utils import HfHubHTTPError
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

    def is_valid(self) -> bool:
        """
        Check whether the languages asked for exist at all
        :return:
        """
        try:
            model_info(self.model_name)
            return True
        except HfHubHTTPError as e:
            if e.response.status_code == 404:
                return False
            raise  # re-raise other errors

    def translate(self, input_string: str) -> str:
        """
        Translate the input_string, using the model in this instance
        :param input_string:
        :return:
        """
        if self.is_valid():
            tokenizer = self.tokenizer_class.from_pretrained(self.model_name)
            model = self.model_class.from_pretrained(self.model_name)
            inputs = tokenizer(
                input_string, return_tensors="pt", padding=True, truncation=True
            )
            translated = model.generate(**inputs)
            output = tokenizer.decode(translated[0], skip_special_tokens=True)
            return output


class TranslatorFactory:
    model_class = MarianMTModel
    tokenizer_class = MarianTokenizer

    @classmethod
    def translator_factory(
        cls, input_lang: LanguageCode, output_lang: LanguageCode
    ) -> Translator:
        return Translator(cls.model_class, cls.tokenizer_class, input_lang, output_lang)
