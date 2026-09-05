from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_predict_endpoint_missing_fields():
    # Sending missing fields should result in 422 Unprocessable Entity
    response = client.post("/api/predict", json={
        "transaction_id": "T1",
        "user_id": "U1"
    })
    assert response.status_code == 422

def test_dashboard_stats():
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "stats" in data
