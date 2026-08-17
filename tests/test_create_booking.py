import pytest

from factories.booking_factory import create_booking_payload
from utils.response_validators import assert_json_content_type, assert_status_code
from utils.schema_validator import validate_schema


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.booking
def test_create_booking(booking_client):
    booking_payload = create_booking_payload(
        totalprice=750,
        depositpaid=True,
    )

    create_response = booking_client.create_booking(booking_payload)

    assert_status_code(create_response, 200)
    assert_json_content_type(create_response)

    response_body = create_response.json()
    validate_schema(response_body, "create_booking_response_schema.json")

    print("Create response:", response_body)
    assert isinstance(response_body, dict)

    assert "bookingid" in response_body
    assert isinstance(response_body["bookingid"], int)
    assert response_body["bookingid"] > 0

    assert "booking" in response_body
    assert isinstance(response_body["booking"], dict)

    created_booking = response_body["booking"]

    assert created_booking == booking_payload

    booking_id = response_body["bookingid"]

    get_response = booking_client.get_booking(booking_id)

    assert_status_code(get_response, 200)
    validate_schema(get_response.json(), "booking_schema.json")
    assert get_response.json() == booking_payload
