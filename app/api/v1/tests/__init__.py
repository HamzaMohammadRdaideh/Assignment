import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_user():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json()["message"] == "Success"
    assert "data" in response.json()


def test_create_user():
    request_body = {
        "username": "test_user",
        "password": "test_password"
    }
    response = client.post("/users/", json=request_body)
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"
    assert "data" in response.json()


def test_create_user_invalid_request():
    request_body = {
        "username": "test_user"
    }
    response = client.post("/users/", json=request_body)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][0]["type"] == "value_error.missing"


def test_login_for_access_token():
    form_data = {
        "username": "test_user",
        "password": "test_password"
    }
    response = client.post("/users/login", data=form_data)
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


def test_login_for_access_token_invalid_credentials():
    form_data = {
        "username": "test_user",
        "password": "wrong_password"
    }
    response = client.post("/users/login", data=form_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"


def test_get_current_user_from_token():
    access_token = "test_access_token"
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"


def test_get_current_user_from_token_invalid_token():
    access_token = "invalid_token"
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid user"


@pytest.fixture(autouse=True)
def mock_user_repository(monkeypatch):
    monkeypatch.setattr("app.api.v1.repositories.user.list_users", mock_list_users)
    monkeypatch.setattr("app.api.v1.repositories.user.create_user", mock_create_user)


def mock_list_users():
    return {"data": []}


def mock_create_user(request_body):
    return {"data": {"username": request_body["username"]}}
