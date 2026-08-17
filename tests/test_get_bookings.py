from utils.response_validators import assert_json_content_type, assert_status_code
from utils.schema_validator import validate_schema


def test_get_all_booking_ids(booking_client):
    response = booking_client.get_all_bookings()

    # print(response.json())

    assert_status_code(response, 200)

    body = response.json()
    validate_schema(body, "booking_ids_schema.json")
    assert isinstance(body, list)
    assert len(body) > 0

    for booking in body:
        assert isinstance(booking, dict)
        assert "bookingid" in booking
        assert isinstance(booking["bookingid"], int)
        assert booking["bookingid"] > 0


    assert_json_content_type(response)

    assert response.elapsed.total_seconds() < 5
