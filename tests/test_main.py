from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from tech_test.app.main import app_factory


@pytest.fixture
def client() -> TestClient:
    return TestClient(app_factory())


def good_data() -> dict:
    return {
        "input_language": "en",
        "output_language": "fr",
        "input_text": "Hello world!",
    }


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world"}


class TestTranslate:
    def test_translate_happy_path(self, client):
        post_data = good_data()
        with patch(
            "tech_test.app.routes.TranslatorFactory.translator_factory"
        ) as translator:
            translator.return_value.is_cached.return_value = True
            response = client.post("/translate", json=post_data)
        response_dict = response.json()
        assert response_dict.get("output_text") == "Coming soon!"

    def test_translate_bad_language(self, client):
        post_data = {
            "input_language": "bob",
            "output_language": "elmo",
            "input_text": "Hello world!",
        }
        response = client.post("/translate", json=post_data)
        assert response.status_code == 422

    def test_model_not_cached(self, client):
        post_data = good_data()
        with patch(
            "tech_test.app.routes.TranslatorFactory.translator_factory"
        ) as translator:
            translator.return_value.is_cached.return_value = False
            response = client.post("/translate", json=post_data)
        assert response.status_code == 202

    def test_invalid_languages(self, client):
        post_data = good_data()
        with patch(
            "tech_test.app.routes.TranslatorFactory.translator_factory"
        ) as translator:
            translator.return_value.is_valid.return_value = False
            translator.return_value.is_cached.return_value = True
            response = client.post("/translate", json=post_data)
        assert response.status_code == 422
        assert (
            response.json()["detail"]["message"]
            == "That language pair doesn't exist right now"
        )
