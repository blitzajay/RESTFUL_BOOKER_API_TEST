import pytest

from clients.auth_client import AuthClient
from clients.booking_client import BookingClient
from config.settings import BOOKER_PASSWORD, BOOKER_USERNAME
from utils.response_validators import assert_status_code


@pytest.fixture(scope="session")
def auth_client():
    client = AuthClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def booking_client():
    client = BookingClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def auth_token(auth_client):
    auth_payload = {
        "username": BOOKER_USERNAME,
        "password": BOOKER_PASSWORD,
    }

    response = auth_client.create_token(auth_payload)

    assert_status_code(response, 200)

    response_body = response.json()

    assert "token" in response_body
    assert response_body["token"].strip() != ""

    return response_body["token"]
