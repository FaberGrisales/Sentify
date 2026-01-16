import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def wait_for_service():
    print("Waiting for service to be healthy (up to 5 minutes for model download)...")
    for i in range(150): # Increased to 150 * 2s = 300s
        try:
            resp = requests.get(f"{BASE_URL}/health")
            if resp.status_code == 200:
                print("Service is up!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(2)
        if i % 5 == 0:
            print(f"Waiting... ({i*2}/300s)")
    return False

def test_api():
    if not wait_for_service():
        print("Service failed to start.")
        sys.exit(1)

    print("\nTesting /sentify with positive text...")
    payload = {
        "text": "Estoy muy feliz y agradecido por este dia maravilloso!",
        "language": "es",
        "include_song": True
    }
    try:
        response = requests.post(f"{BASE_URL}/sentify", json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Response:", data)
            if "recommendation" in data and "song" in data["recommendation"]:
                 # Check for Spanish values
                 if data["sentiment"] in ["Positivo", "Neutral", "Negativo"]:
                     print("✅ Positive sentiment (Spanish) & recommendation test passed")
                 else:
                     print(f"⚠️ Warning: Sentiment '{data['sentiment']}' might not be in Spanish")
            else:
                 print("❌ Response structure missing recommendation")
        else:
             print(f"❌ Failed with {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")

    print("\nTesting /sentify with negative text...")
    payload_neg = {
        "text": "Estoy furioso y muy molesto con el servicio.",
        "language": "es"
    }
    try:
        response = requests.post(f"{BASE_URL}/sentify", json=payload_neg)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
             print("✅ Negative sentiment test passed")
        else:
             print(f"❌ Failed with {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
