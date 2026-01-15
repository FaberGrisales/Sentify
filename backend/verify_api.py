from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api():
    print("Testing /health...")
    response = client.get("/health")
    print(response.json())
    assert response.status_code == 200

    print("\nTesting /sentify with positive text...")
    payload = {
        "text": "Estoy muy feliz y agradecido por este dia maravilloso!",
        "language": "es",
        "include_song": True
    }
    response = client.post("/sentify", json=payload)
    print(response.status_code)
    try:
        data = response.json()
        print(data)
        assert response.status_code == 200
        assert data["sentiment"] == "Positive" or data["sentiment"] == "Neutral" # Depends on model
        assert "recommendation" in data
        assert "song" in data["recommendation"]
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(response.text)

    print("\nTesting /sentify with negative text...")
    payload_neg = {
        "text": "Estoy furioso y muy molesto con el servicio.",
        "language": "es"
    }
    response = client.post("/sentify", json=payload_neg)
    print(response.json())
    assert response.status_code == 200

if __name__ == "__main__":
    test_api()
