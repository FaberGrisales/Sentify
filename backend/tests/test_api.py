import pytest

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "running"

@pytest.mark.parametrize("payload", [
    {
        "text": "Estoy muy feliz y agradecido por este dia maravilloso!",
        "language": "es",
        "include_song": True
    },
    {
        "text": "Estoy furioso y muy molesto con el servicio.",
        "language": "es"
    }
])
def test_sentify_endpoint(client, payload):
    response = client.post("/sentify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert "score" in data
    assert "emotions" in data
    assert "recommendation" in data
    
    if payload.get("include_song"):
        assert "song" in data["recommendation"]

def test_emotions_endpoint(client):
    response = client.get("/api/v1/emotions")
    assert response.status_code == 200
    data = response.json()
    assert "emotions" in data
    assert len(data["emotions"]) > 0
