import pytest
from fastapi.testclient import TestClient

from tech_test.app.main import app_factory


@pytest.fixture
def client() -> TestClient:
    return TestClient(app_factory())


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world"}


class TestTranslate:
    def test_translate_happy_path(self, client):
        post_data = {
            "input_language": "en",
            "output_language": "fr",
            "input_text": "Hello world!",
        }
        response = client.post("/translate", json=post_data)
        response_dict = response.json()
        assert response_dict["output_text"] == "Coming soon!"

    def test_translate_bad_language(self, client):
        post_data = {
            "input_language": "bob",
            "output_language": "elmo",
            "input_text": "Hello world!",
        }
        response = client.post("/translate", json=post_data)
        assert response.status_code == 422
