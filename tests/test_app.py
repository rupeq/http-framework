import pytest

from example.app import app, api
from http_framework.test_client import TestClient


@pytest.fixture
def client():
    app.register_blueprint(api)
    return TestClient(app)


def test_index_route(client):
    response = client.get("/api/v1/")
    assert response.status == 200
    assert response.json == {"message": "Hello World!", "query": {}}


def test_create_document(client):
    data = {"content": "Test document content"}
    response = client.post("/api/v1/documents/1/versions/1.0", data=data)
    assert response.status == 200
    assert response.json == {
        "message": "Document created!",
        "id": 1,
        "version_id": "1.0",
        "body": data,
    }
