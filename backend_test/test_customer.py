import pytest
import re
from requests import Session
from typing import Any
from datetime import date, timedelta


@pytest.fixture(scope="session")
def shared_data() -> dict[str, Any]:
  return {}


@pytest.mark.dependency(depends=["backend_test/test_user.py::test_create_user"], scope="session")
def test_create_customer(base_url: str, user_sub: str, user_session: Session, customer_session_data: dict[str, Any]) -> None:
    url = f"{base_url}/api/user/{user_sub}/customer"
    payload = {
        "sub": user_sub,
        "company_name": "Acme Corp",
        "email": "unique_email@example.com",   
    }
    response = user_session.post(url, json=payload)
    assert response.status_code == 201
    assert "customer_id" in response.json()
    customer_data = response.json()
    customer_session_data.update(customer_data)


@pytest.mark.dependency(depends=["test_create_customer"])
def test_update_customer(base_url: str, user_sub: str, user_session: Session, customer_session_data: dict[str, Any]) -> None:
    assert "customer_id" in customer_session_data
    assert "user_id" in customer_session_data
    customer_id = customer_session_data["customer_id"]
    payload = {
       "sub": user_sub,
       "customer_id": customer_id,
       "phone":"123-456-7890",
       "email":"updated@email.com"
    }
    url = f"{base_url}/api/user/{user_sub}/customer/{customer_id}"
    response = user_session.put(url, json=payload)
    assert response.status_code == 200


@pytest.mark.dependency(depends=["test_create_customer"])
def test_get_customer(base_url: str, user_sub: str, user_session: Session, customer_session_data: dict[str, Any]) -> None:
    assert "customer_id" in customer_session_data
    customer_id = customer_session_data["customer_id"]
    user_sub = user_session.params.get("sub", user_sub)
    assert "user_id" in customer_session_data
    url = f"{base_url}/api/user/{user_sub}/customer/{customer_id}"
    response = user_session.get(url)
    assert response.status_code == 200


@pytest.mark.dependency(depends=["test_create_customer"])
def test_list_customers_by_sub(base_url: str, user_sub: str, user_session: Session) -> None:
    url = f"{base_url}/api/user/{user_sub}/customers"
    response = user_session.get(url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.dependency(depends=["test_create_customer"])
def test_delete_customer(base_url: str, user_sub: str, user_session: Session, customer_session_data: dict[str, Any]) -> None:
    assert "customer_id" in customer_session_data
    customer_id = customer_session_data["customer_id"]
    user_sub = user_session.params.get("sub", user_sub)
    url = f"{base_url}/api/user/{user_sub}/customer/{customer_id}"
    response = user_session.delete(url)
    assert response.status_code == 200
    assert response.json()["message"] == "Customer deleted successfully"

