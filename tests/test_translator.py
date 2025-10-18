from tech_test.services.translator import Translator, TranslatorFactory


class TestFactory:
    def test_factory_happy_path(self):
        en_fr_translator = TranslatorFactory.translator_factory("en", "fr")
        assert isinstance(en_fr_translator, Translator)
