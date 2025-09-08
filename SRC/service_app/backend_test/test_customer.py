import pytest
import re
from requests import Session
from typing import Any
from datetime import date, timedelta

@pytest.mark.dependency(depends=["backend_test/test_user.py::test_create_user"], scope="session")
def test_create_customer(base_url: str, user_sub: str, user_session: Session, user_session_data:dict[str, any]) -> None:
    print("user_session_data before test_create_customer:", user_session_data)
    # url = f"{base_url}/user"
    # payload = {
    #     "sub": user_sub,
    #     "email": user_session_data["email"],
    #     "first_name": user_session_data["first_name"],
    #     "last_name": user_session_data["last_name"],
    #     "birthdate": str(date.today() - timedelta(days=365*30)),  # 30 years ago
    # }
    # response = user_session.post(url, json=payload)
    # print('Cust-recreated', response.json())

    url = f"{base_url}/user/{user_sub}/customer"
    payload = {
        "sub": user_sub,
        "company_name": "Acme Corp",
        "email": "unique_email@example.com",   
    }
    response = user_session.post(url, json=payload)
    print("Create Customer Response:", response.json())
    assert response.status_code == 201
    assert "customer_id" in response.json()
    customer_data = response.json()
    print("Created customer:", customer_data)