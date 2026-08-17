import pytest

from factories.booking_factory import create_booking_payload
from utils.response_validators import assert_json_content_type, assert_status_code
from utils.schema_validator import validate_schema


@pytest.mark.regression
@pytest.mark.booking
def test_partial_update_booking(booking_client, auth_token):
    original_payload = create_booking_payload()

    create_response = booking_client.create_booking(original_payload)

    assert_status_code(create_response, 200)

    booking_id = create_response.json()["bookingid"]

    # Only these fields should change.
    partial_payload = {
        "totalprice": 950,
        "depositpaid": True,
        "additionalneeds": "Late checkout",
    }

    # Act: partially update the booking.
    patch_response = booking_client.partial_update_booking(
        booking_id,
        partial_payload,
        auth_token,
    )

    assert_status_code(patch_response, 200)
    assert_json_content_type(patch_response)

    updated_booking = patch_response.json()
    validate_schema(updated_booking, "booking_schema.json")

    print("PATCH response:", updated_booking)

    # Changed fields
    assert updated_booking["totalprice"] == 950
    assert updated_booking["depositpaid"] is True
    assert updated_booking["additionalneeds"] == "Late checkout"

    # Unchanged fields
    assert updated_booking["firstname"] == original_payload["firstname"]
    assert updated_booking["lastname"] == original_payload["lastname"]
    assert updated_booking["bookingdates"] == original_payload["bookingdates"]

    # Verify persisted state.
    get_response = booking_client.get_booking(booking_id)

    assert_status_code(get_response, 200)
    assert get_response.json() == updated_booking







