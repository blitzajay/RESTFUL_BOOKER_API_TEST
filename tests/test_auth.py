import requests
import pytest
from config.settings import BASE_URL, DEFAULT_TIMEOUT


def test_create_auth_token():
    auth_payload = {
        "username": "admin",
        "password": "password123",
    }

    response = requests.post(
        BASE_URL + "/auth",
        json=auth_payload,
        headers={"Accept": "application/json"},
        timeout=DEFAULT_TIMEOUT,
    )

    print("Auth response:", response.json())

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]

    response_body = response.json()

    assert isinstance(response_body, dict)
    assert "token" in response_body
    assert isinstance(response_body["token"], str)
    assert response_body["token"].strip() != ""


@pytest.mark.xfail(
    reason="Known API defect: invalid credentials return 200 instead of 401",
    strict=True,
)
def test_authentication_with_invalid_credentials():
    invalid_payload = {
        "username": "wrong-user",
        "password": "wrong-password",
    }

    response = requests.post(
        BASE_URL + "/auth",
        json=invalid_payload,
        timeout=DEFAULT_TIMEOUT,
    )

    assert response.status_code == 401

    response_body = response.json()

    assert "reason" in response_body
    assert response_body["reason"] == "Bad credentials"
    assert "token" not in response_body