import requests

from config.settings import BASE_URL, DEFAULT_TIMEOUT

def test_get_booking_by_id():
    # First request: obtain valid booking IDs

    list_response = requests.get(BASE_URL+"/booking", timeout=DEFAULT_TIMEOUT)
    assert list_response.status_code == 200

    bookings = list_response.json()
    assert len(bookings) > 0

    booking_id = bookings[0]["bookingid"]

    # Second request: retrieve the selected booking

    booking_response = requests.get(f"{BASE_URL}/booking/{booking_id}", timeout=DEFAULT_TIMEOUT)

    assert booking_response.status_code == 200

    booking = booking_response.json()

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

    assert "application/json" in booking_response.headers["Content-Type"]
    assert booking_response.elapsed.total_seconds() < 5



def test_get_nonexisting_booking():
    nonexisting_booking_id = 999999999

    response = requests.get(f"{BASE_URL}/booking/{nonexisting_booking_id}", timeout=DEFAULT_TIMEOUT)

    print("Status code : ", response.status_code)
    print("Response : ", response.text)

    assert response.status_code == 404