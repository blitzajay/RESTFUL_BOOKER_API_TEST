from factories.booking_factory import create_booking_payload
from utils.response_validators import assert_json_content_type, assert_status_code
from utils.schema_validator import validate_schema


def test_update_complete_booking(booking_client, auth_token):
    original_payload = create_booking_payload()

    # Arrange: create a booking.
    create_response = booking_client.create_booking(original_payload)

    assert_status_code(create_response, 200)

    booking_id = create_response.json()["bookingid"]

    updated_payload = create_booking_payload(
        firstname="UpdatedAjay",
        lastname="UpdatedKumar",
        totalprice=900,
        depositpaid=True,
        bookingdates={
            "checkin": "2026-11-01",
            "checkout": "2026-11-10",
        },
        additionalneeds="Late checkout",
    )

    # Act: completely replace the booking.
    update_response = booking_client.update_booking(
        booking_id,
        updated_payload,
        auth_token,
    )

    print("Update response:", update_response.json())

    # Assert the update response.
    assert_status_code(update_response, 200)
    assert_json_content_type(update_response)
    validate_schema(update_response.json(), "booking_schema.json")
    assert update_response.json() == updated_payload

    # Verify the persisted booking.
    get_response = booking_client.get_booking(booking_id)

    assert_status_code(get_response, 200)
    assert get_response.json() == updated_payload
