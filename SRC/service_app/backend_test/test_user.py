import pytest
import re
from requests import Session
from typing import Any
from datetime import date, timedelta


@pytest.mark.dependency()
def test_create_user(base_url: str, user_sub: str, user_session: Session) -> None:
  url = f"{base_url}/user"
  payload = {
    "sub": user_sub,
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "birthdate": str(date.today() - timedelta(days=365*30)),  # 30 years ago
  }
  response = user_session.post(url, json=payload)
  print(response.text)
  assert response.status_code == 200
  assert "user_id" in response.json()["user"]