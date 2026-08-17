import pytest

from utils.response_validators import assert_json_content_type, assert_status_code

def test_create_auth_token(auth_client):
    auth_payload = {
        "username": "admin",
        "password": "password123",
    }

    response = auth_client.create_token(auth_payload)

    print("Auth response:", response.json())

    assert_status_code(response, 200)
    assert_json_content_type(response)

    response_body = response.json()

    assert isinstance(response_body, dict)
    assert "token" in response_body
    assert isinstance(response_body["token"], str)
    assert response_body["token"].strip() != ""


@pytest.mark.xfail(
    reason="Known API defect: invalid credentials return 200 instead of 401",
    strict=True,
)
def test_authentication_with_invalid_credentials(auth_client):
    invalid_payload = {
        "username": "wrong-user",
        "password": "wrong-password",
    }

    response = auth_client.create_token(invalid_payload)

    assert_status_code(response, 401)

    response_body = response.json()

    assert "reason" in response_body
    assert response_body["reason"] == "Bad credentials"
    assert "token" not in response_body
