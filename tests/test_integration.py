from tech_test.services.languages import LanguageCode

from .conftest import good_data


class TestTranslation:

    def test_not_cached(self, client, hf_cache_dir):
        post_data = good_data()
        post_data["input_language"] = "fr"
        post_data["output_language"] = "en"
        response = client.post("/translate", json=post_data)
        assert response.status_code == 202

    def test_happy_path(self, client, hf_cache_dir):
        from tech_test.services.translator import TranslatorFactory

        TranslatorFactory.translator_factory(
            LanguageCode("en"), LanguageCode("fr")
        ).pull_models()
        response = client.post("/translate", json=good_data())
        assert response.json()["output_text"] == "Bonjour le monde !"

    def test_not_valid_pair(self, client):
        post_data = good_data()
        post_data["output_language"] = "en"
        response = client.post("/translate", json=post_data)
        assert response.status_code == 422
