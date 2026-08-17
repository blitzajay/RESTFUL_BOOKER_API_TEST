import pytest

from utils.response_validators import assert_json_content_type, assert_status_code
from utils.schema_validator import validate_schema


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.booking
def test_get_booking_by_id(booking_client):
    # First request: obtain valid booking IDs

    list_response = booking_client.get_all_bookings()
    assert_status_code(list_response, 200)

    bookings = list_response.json()
    assert len(bookings) > 0

    booking_id = bookings[0]["bookingid"]

    # Second request: retrieve the selected booking

    booking_response = booking_client.get_booking(booking_id)

    assert_status_code(booking_response, 200)

    booking = booking_response.json()
    validate_schema(booking, "booking_schema.json")

    print("Booking ID : ", booking_id)
    print("Booking : ", booking)


    assert isinstance(booking, dict)

    assert "firstname" in booking
    assert isinstance(booking["firstname"], str)
    assert booking["firstname"].strip() != ""

    assert "lastname" in booking
    assert isinstance(booking["lastname"], str)

    assert "totalprice" in booking
    assert isinstance(booking["totalprice"], int)
    assert booking["totalprice"] >= 0

    assert "depositpaid" in booking
    assert isinstance(booking["depositpaid"], bool)
    assert "bookingdates" in booking

    assert isinstance(booking["bookingdates"], dict)

    booking_dates = booking["bookingdates"]

    assert "checkin" in booking_dates
    assert "checkout" in booking_dates
    assert isinstance(booking_dates["checkin"], str)
    assert isinstance(booking_dates["checkout"], str)

    assert_json_content_type(booking_response)
    assert booking_response.elapsed.total_seconds() < 5



@pytest.mark.regression
@pytest.mark.booking
@pytest.mark.negative
def test_get_nonexisting_booking(booking_client):
    nonexisting_booking_id = 999999999

    response = booking_client.get_booking(nonexisting_booking_id)

    print("Status code : ", response.status_code)
    print("Response : ", response.text)

    assert_status_code(response, 404)
