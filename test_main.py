from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_shorten():
    response = client.post(
        "/shorten",
        json={"name": "dinolozina.eu2"})
    assert response.status_code == 200
    assert response.json() == {"name": "dinolozina.eu"}


def test_read_main():
    response = client.get("/xyz")
    assert response.status_code == 200
    assert response.json() == {"short_url": "xyz"}
