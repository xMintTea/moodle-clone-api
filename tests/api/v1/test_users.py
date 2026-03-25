from fastapi.testclient import TestClient

from app.api.v1.users import get_user_service
from app.main import app
from app.service.user_service import UserService
from tests.test_db import TestingSessionLocal

# Setup test client
client = TestClient(app)


def override_get_user_service():
    session = TestingSessionLocal()
    yield UserService(session)


app.dependency_overrides[get_user_service] = override_get_user_service

def test_create_user():
    # Create a new user
    response = client.post("/v1/users", json={
  "first_name": "string",
  "middle_name": "string",
  "last_name": "string",
  "user_type": "Студент",
  "user_status": "Активен",
  "password": "stringst",
  "email": "user@example.com"
})

    assert response.status_code == 201


def test_list_users_after_creation():
    response = client.get("/v1/users")
    
    assert len(response.json()) == 1


# ---- first_name field testing ----

def test_update_user_firstname():
    response = client.put("/v1/users/1",json={
        "first_name": "TEST",
    })
    
    assert response.status_code == 200
    assert response.json()["first_name"] == "TEST"


def test_update_user_empty_request_body():
    response = client.put("/v1/users/1", json={})
    
    assert response.status_code == 200
    assert response.json()["first_name"] == "TEST"


def test_user_first_name_none():
    response = client.put("/v1/users/1", json={
        "first_name" : None
    })
    
    assert response.status_code == 500
    
def test_user_first_name_lenght_too_short():
    response = client.put("/v1/users/1", json={
        "first_name" : ""
    })
    
    assert response.status_code == 422
    
    response = client.put("/v1/users/1", json={
        "first_name" : "a"
    })
    
    assert response.status_code == 422
    
def test_user_first_name_too_long():
    response = client.put("/v1/users/1", json={
        "first_name" : "a"*51
    })
    
    assert response.status_code == 422