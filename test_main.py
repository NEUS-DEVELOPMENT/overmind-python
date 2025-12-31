from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Verifies the system is operational."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Overmind Operational", "mode": "Sovereign"}

def test_lethal_decision_logic():
    """Simulates a high-risk threat to test Lethal Mode activation."""
    payload = {
        "sentinel_id": "SENTINEL-01",
        "threat_signature": "SQL_INJECTION_HEURISTIC",
        "risk_score": 9  # High score should trigger lethal response
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Validation: Ensure the Overmind generated a weapon
    assert data["action"] == "LETHAL_INJECTION"
    assert len(data["payload_data"]) > 0  # Payload must verify content existence
