from fastapi.testclient import TestClient
from tech_test.app.main import app_factory

def test_index():
    app = app_factory()
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world"}