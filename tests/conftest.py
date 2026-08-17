import pytest
import requests


BASE_URL = "https://restful-booker.herokuapp.com"


@pytest.fixture(scope="session")
def auth_token():
    auth_payload = {
        "username": "admin",
        "password": "password123",
    }

    response = requests.post(
        BASE_URL + "/auth",
        json=auth_payload,
        timeout=10,
    )

    assert response.status_code == 200

    response_body = response.json()

    assert "token" in response_body
    assert response_body["token"].strip() != ""

    return response_body["token"]