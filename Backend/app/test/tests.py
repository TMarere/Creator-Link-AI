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
        "userName": "Tanatswa"
    })
    assert response.status_code == 200
    payload = response.json()
    
    assert payload["userName"] == "Tanatswa"

    list_response = client.get("/users/")
    assert list_response.status_code == 200
    users = list_response.json()
    assert any(user["email"] == "test@test.com" for user in users)
