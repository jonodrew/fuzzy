from unittest.mock import patch

from huggingface_hub.errors import HfHubHTTPError
from requests import Request, Response

from tech_test.services.translator import Translator, TranslatorFactory


class TestFactory:
    def test_factory_happy_path(self):
        en_fr_translator = TranslatorFactory.translator_factory("en", "fr")
        assert isinstance(en_fr_translator, Translator)


class TestTranslater:
    def test_is_cached(self):
        with patch(
            "tech_test.services.translator.AutoModel.from_pretrained"
        ) as mock_func:
            mock_func.side_effect = OSError("No such model")
            translator = TranslatorFactory.translator_factory("en", "fr")
            assert not translator.is_cached()

    def test_is_valid(self):
        with patch("tech_test.services.translator.model_info") as mock_func:
            fake_response = Response()
            fake_response.status_code = 404
            fake_response._content = b"Not found"

            fake_request = Request(
                method="GET", url="https://huggingface.co/api/models/foo"
            ).prepare()
            fake_response.request = fake_request

            exc = HfHubHTTPError("Mocked 404", response=fake_response)

            mock_func.side_effect = exc
            translator = TranslatorFactory.translator_factory("en", "fr")
            assert not translator.is_valid()
