from pathlib import Path

db_path = Path(__file__).resolve().parents[2] / "creatorlink.db"
if db_path.exists():
    db_path.unlink()

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "email": "test@test.com",
        "userName": "Tanatswa",
        "niche": "gaming",
        "instagram": "@test",
        "youtube": "yt",
        "tiktok": "tt"
    })
    assert response.status_code == 200
    payload = response.json()
    
    assert payload["userName"] == "Tanatswa"
    assert payload["niche"] == "gaming"

    list_response = client.get("/users/")
    assert list_response.status_code == 200
    users = list_response.json()
    assert any(user["userName"] == "Tanatswa" for user in users)
    assert any(user["niche"] == "gaming" for user in users)
