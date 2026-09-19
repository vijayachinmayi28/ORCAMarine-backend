from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ask_demo():
    response = client.post(
        "/ask",
        json={
            "location": "Mumbai Coast",
            "question": "Is it safe to swim today?",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["location"]["latitude"] == 19.076
    assert data["marine"]["wave_height_m"] == 1.2
    assert "safety" in data
    assert data["demo_mode"] is True
