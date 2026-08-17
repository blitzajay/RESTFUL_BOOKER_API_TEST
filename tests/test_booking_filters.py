import pytest

from factories.booking_factory import create_booking_payload
from utils.response_validators import assert_json_content_type, assert_status_code
from utils.schema_validator import validate_schema


@pytest.mark.regression
@pytest.mark.booking
def test_filter_bookings_by_name(booking_client):
    # Create unique names to avoid matching another user's booking.

    booking_payload = create_booking_payload(depositpaid=True)

    firstname = booking_payload["firstname"]
    lastname = booking_payload["lastname"]

    # Arrange: create our own booking.
    create_response = booking_client.create_booking(booking_payload)

    assert_status_code(create_response, 200)

    created_booking = create_response.json()

    assert "bookingid" in created_booking
    assert isinstance(created_booking["bookingid"], int)

    booking_id = created_booking["bookingid"]

    # Act: filter bookings using the unique names.
    params = {
        "firstname": firstname,
        "lastname": lastname,
    }

    filter_response = booking_client.get_all_bookings(params=params)

    print("Request URL:", filter_response.url)
    print("Filtered response:", filter_response.json())

    # Assert: validate the filtered response.
    assert_status_code(filter_response, 200)
    assert_json_content_type(filter_response)

    filtered_bookings = filter_response.json()
    validate_schema(filtered_bookings, "booking_ids_schema.json")

    assert isinstance(filtered_bookings, list)
    assert len(filtered_bookings) > 0

    returned_booking_ids = []

    for booking in filtered_bookings:
        assert isinstance(booking, dict)
        assert "bookingid" in booking
        assert isinstance(booking["bookingid"], int)

        returned_booking_ids.append(booking["bookingid"])

    assert booking_id in returned_booking_ids
