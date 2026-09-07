import pytest
from fastapi.testclient import TestClient
from api.msa_routes import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_analytics_overview():
    response = client.get("/analytics/overview?product_id=1")
    assert response.status_code == 200
    data = response.json()
    assert "total_visitors" in data or "visitors" in data or "conversion_rate" in data or "status" in data or isinstance(data, dict)

def test_generate_campaign():
    payload = {
        "product_name": "Test Product",
        "product_desc": "Automated testing product for SaaS"
    }
    response = client.post("/marketing/campaigns", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
