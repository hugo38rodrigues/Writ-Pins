import json
from fastapi.testclient import TestClient

from main import app, db, User

client = TestClient(app)

def test_create_user():
    # Test successful user creation
    new_user = {
        "id": 1,
        "name": "John",
        "surname": "Doe",
        "password": "testpassword",
        "email": "john.doe@example.com",
        "birthdate": "1990-01-01"
    }
    response = client.post("/users/", json=new_user)
    assert response.status_code == 200
    assert response.json() == new_user
    assert len(db) == 1
    assert db[0].id == new_user["id"]

def test_read_user():
    # Test successful user read
    new_user = {
        "id": 1,
        "name": "John",
        "surname": "Doe",
        "password": "testpassword",
        "email": "john.doe@example.com",
        "birthdate": "1990-01-01"
    }
    db.append(User(**new_user))
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == new_user

    # Test user not found
    response = client.get("/users/2")
    assert response.status_code == 404

def test_update_user():
    # Test successful user update
    new_user = {
        "id": 1,
        "name": "John",
        "surname": "Doe",
        "password": "testpassword",
        "email": "john.doe@example.com",
        "birthdate": "1990-01-01"
    }
    db.append(User(**new_user))
    updated_user = {
        "id": 1,
        "name": "Jane",
        "surname": "Doe",
        "password": "newpassword",
        "email": "jane.doe@example.com",
        "birthdate": "1990-02-02"
    }
    response = client.put("/users/1", json=updated_user)
    assert response.status_code == 200
    assert response.json() == updated_user
    assert len(db) == 1
    assert db[0].name == updated_user["name"]

    # Test user not found
    response = client.put("/users/2", json=updated_user)
    assert response.status_code == 404

def test_delete_user():
    # Test successful user deletion
    new_user = {
        "id": 1,
        "name": "John",
        "surname": "Doe",
        "password": "testpassword",
        "email": "john.doe@example.com",
        "birthdate": "1990-01-01"
    }
    db.append(User(**new_user))
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}
    assert len(db) == 0

    # Test user not found
    response = client.delete("/users/2")
    assert response.status_code == 404
