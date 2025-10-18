from unittest.mock import patch

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
