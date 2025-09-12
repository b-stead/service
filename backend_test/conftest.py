import pytest
import subprocess
import time
from datetime import timedelta, datetime
import jwt
import requests
from typing import Any
from collections.abc import Generator
import os

BASE_URL = "http://localhost:8000"
TEST_SUB = "somerandomstring"
USER_SUB = "testuser"


def create_access_token(data: dict[Any, Any], lifetime: timedelta = timedelta(seconds=3600)) -> str:
  """Create a signed access token from the provided data"""
  _data = data.copy()
  expires = datetime.now() + lifetime
  _data.update({'exp': expires})
  return jwt.encode(_data, 'foo', algorithm='HS256')  # where 'foo' is the secret key used in the backend


@pytest.fixture(scope="session", autouse=True)
def base_url() -> str:
  return BASE_URL

@pytest.fixture(scope="session", autouse=True)
def sub() -> str:
  """sub for the main test user with pre-generated test data"""
  return TEST_SUB


@pytest.fixture(scope="session", autouse=True)
def user_sub() -> str:
  """sub for testing user create/update/delete"""
  return USER_SUB


@pytest.fixture(scope="session")
def session_data() -> dict[str, Any]:
  """session data for the main test user with pre-generated test data"""
  return {}


@pytest.fixture(scope="session")
def user_session_data() -> dict[str, Any]:
  """session data for testing user create/update/delete"""
  return {}


@pytest.fixture(scope="session", autouse=True)
def session() -> Generator[requests.Session, None, None]:
  """session for the main test user with pre-generated test data"""
  global Session
  Session = requests.Session()
  Session.headers.update({"Authorization": f"Bearer {create_access_token(data={'sub': TEST_SUB})}"})
  yield Session
  Session.close()


@pytest.fixture(scope="session", autouse=True)
def user_session() -> Generator[requests.Session, None, None]:
  """session for testing user create/update/delete"""
  global UserSession
  UserSession = requests.Session()
  UserSession.headers.update({"Authorization": f"Bearer {create_access_token(data={'sub': USER_SUB})}"})
  yield UserSession
  UserSession.close()

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown() -> Generator[None, None, None]:
  # Start Docker Compose
  env = os.environ.copy()
  env["TEST_ENVIRONMENT"] = "true"
  subprocess.run([
    "docker",
    "compose",
    "--project-directory=.",
    "--project-name=service-app",
    "--file=repository/compose.yaml",
    "--file=backend/compose.yaml",
    "up",
    "--detach"
  ], check=True, env=env)
  # Wait for the service to be ready
  iteration = 0
  while True:
    try:
      response = requests.get(f"{BASE_URL}/healthz", timeout=1)
      response.raise_for_status()
      print(response.text)
      break
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as err:
      print(err)
      time.sleep(1)
      iteration += 1
      if iteration > 30:
        raise TimeoutError("Service did not start in time")
      
  # Apply schema
  subprocess.run([
    "atlas",
    "schema",
    "apply",
    "--auto-approve",
    "--url=postgresql://postgres:password@localhost:5432/postgres?sslmode=disable",
    "--to=file://repository/schema/schema.sql",
    "--dev-url=docker://postgres/16"
  ], check=True)

  # Insert generated data
#   subprocess.run([
#     "psql",
#     "-v",
#     "ON_ERROR_STOP=1",
#     "--file=repository/testdata/generated.sql",
#     "postgresql://postgres:password@localhost:5432/postgres?sslmode=disable"
#   ], check=True)

  # Insert test data
  subprocess.run([
    "psql",
    "-v",
    "ON_ERROR_STOP=1",
    "--file=repository/testdata/testdata.sql",
    "postgresql://postgres:password@localhost:5432/postgres?sslmode=disable"
  ], check=True)

  yield

  subprocess.run(["docker", "logs", "service-app-backend-1"])
  # subprocess.run(["docker", "logs", "service-app-worker-1"])

  # Stop Docker Compose
  subprocess.run(["docker", "compose", "--project-name=service-app", "down"], check=True)