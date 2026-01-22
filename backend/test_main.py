from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Travel Story API"}

def test_create_user():
    unique_email = f"test_{uuid.uuid4()}@example.com"
    response = client.post(
        "/create-account",
        json={"fullName": "Test User", "email": unique_email, "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == unique_email
    assert "accessToken" in data

def test_login():
    # first create a user
    unique_email = f"login_{uuid.uuid4()}@example.com"
    client.post(
        "/create-account",
        json={"fullName": "Login User", "email": unique_email, "password": "password123"}
    )
    
    response = client.post(
        "/login",
        json={"email": unique_email, "password": "password123"}
    )
    assert response.status_code == 200
    assert "accessToken" in response.json()

def test_create_story():
    # Create user and get token
    unique_email = f"story_{uuid.uuid4()}@example.com"
    reg_res = client.post(
        "/create-account",
        json={"fullName": "Story User", "email": unique_email, "password": "password123"}
    )
    token = reg_res.json()["accessToken"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post(
        "/add-story",
        json={
            "title": "My Trip",
            "story": "It was amazing",
            "visitedLocation": ["Paris", "France"],
            "imageUrl": "http://example.com/image.jpg",
            "visitedDate": "2023-10-27T10:00:00"
        },
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "My Trip"
