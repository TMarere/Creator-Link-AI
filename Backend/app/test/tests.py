from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "email": "test@test.com",
        "userName": "Tanatswa"
    })
    assert response.status_code == 200