import pytest
import re
from requests import Session
from typing import Any
from datetime import date, timedelta


@pytest.mark.dependency()
def test_create_user(base_url: str, user_sub: str, user_session: Session, user_session_data: dict[str, Any]) -> None:
  url = f"{base_url}/user"
  print('usr_url:', url)
  payload = {
    "sub": user_sub,
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "birthdate": str(date.today() - timedelta(days=365*30)),  # 30 years ago
  }
  response = user_session.post(url, json=payload)
  print("Create User Response:", response.json())
  assert response.status_code == 200
  assert "user_id" in response.json()["user"]
  user_data = response.json()["user"]
  user_session_data.update(user_data)


@pytest.mark.dependency()
def test_create_user_again(base_url: str, user_sub: str, user_session: Session) -> None:
  url = f"{base_url}/user"
  payload = {
    "sub": user_sub,
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "birthdate": str(date.today() - timedelta(days=365*30)),  # 30 years ago
  }
  response = user_session.post(url, json=payload)
  assert response.status_code == 406


@pytest.mark.dependency(depends=["test_create_user"])
def test_get_user(base_url: str, user_sub: str, user_session: Session) -> None:
  url = f"{base_url}/user/{user_sub}"
  response = user_session.get(url)
  assert response.status_code == 200
  assert response.json()["sub"] == user_sub
  assert re.match(r"[^@]+@[^@]+\.[^@]+", response.json()["email"])
  assert response.json()["first_name"] == "John"


@pytest.mark.dependency(depends=["backend_test/test_user.py::test_create_user"], scope="session")
def test_get_another_user(base_url: str, user_sub: str, user_session: Session) -> None:
  url = f"{base_url}/user/foo"
  session = user_session
  print('session:',session.headers)
  response = user_session.get(url)
  # change to 401 when auth is implemented
  assert response.status_code == 500
  # assert response.status_code == 401


@pytest.mark.dependency(depends=[
  "test_create_user_again",
  "test_get_user",
  "test_get_another_user"
])
def test_delete_user(base_url: str, user_sub: str, user_session: Session) -> None:
  url = f"{base_url}/user/{user_sub}"
  response = user_session.delete(url)
  assert response.status_code == 200


@pytest.mark.dependency(depends=[
  "test_create_user",
  "test_delete_user"
])
def test_recreate_user(base_url: str, user_sub: str, user_session: Session, user_session_data: dict[str, Any]) -> None:
  url = f"{base_url}/user"
  payload = {
    "sub": user_sub,
    "email": user_session_data["email"],
    "first_name": user_session_data["first_name"],
    "last_name": user_session_data["last_name"],
    "birthdate": str(date.today() - timedelta(days=365*30)),  # 30 years ago
  }
  response = user_session.post(url, json=payload)
  print('recreated', response.json())
  assert response.status_code == 200
  assert "user_id" in response.json()["user"]

  # Update user_session_data with the recreated user's data
  user_data = response.json()["user"]
  user_session_data.update(user_data)

