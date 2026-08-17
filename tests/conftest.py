import pytest
import requests

from config.settings import BASE_URL, DEFAULT_TIMEOUT


@pytest.fixture(scope="session")
def auth_token():
    auth_payload = {
        "username": "admin",
        "password": "password123",
    }

    response = requests.post(
        BASE_URL + "/auth",
        json=auth_payload,
        timeout=DEFAULT_TIMEOUT,
    )

    assert response.status_code == 200

    response_body = response.json()

    assert "token" in response_body
    assert response_body["token"].strip() != ""

    return response_body["token"]
