import pytest
from requests import Session
from typing import Any
from datetime import date


@pytest.fixture(scope="module")
def shared_data() -> dict[str, Any]:
    return {}


@pytest.mark.dependency(depends=["backend_test/test_customer.py::test_create_customer"], scope="session")
def test_create_job(base_url: str, user_sub: str, user_session: Session, customer_session_data: dict[str, Any]) -> None:
    url = f"{base_url}/api/user/{user_sub}/job"
    customer_id = customer_session_data.get("customer_id")
    print("id", customer_id)
    assert customer_id is not None, "customer_id must be set in  customer_Session_data"
    payload = {
        "sub": user_sub,
        "customer_id": customer_id,
        "job_title": "Test Job",
        "start_date": str(date.today()),
        "end_date": None,
        "job_description": "Do a test job."
    }
    response = user_session.post(url, json=payload)
    print("Create Job Response:", response.json())
    assert response.status_code == 201
    assert "job_id" in response.json()
    # job_session_data = response.json()
