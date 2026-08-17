from uuid import uuid4

import requests

from config.settings import BASE_URL, DEFAULT_TIMEOUT


def test_filter_bookings_by_name():
    # Create unique names to avoid matching another user's booking.
    unique_value = uuid4().hex[:8]

    firstname = f"Ajay{unique_value}"
    lastname = f"Kumar{unique_value}"

    booking_payload = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": 500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-09-01",
            "checkout": "2026-09-05",
        },
        "additionalneeds": "Breakfast",
    }

    # Arrange: create our own booking.
    create_response = requests.post(
        BASE_URL + "/booking",
        json=booking_payload,
        headers={"Accept": "application/json"},
        timeout=DEFAULT_TIMEOUT,
    )

    assert create_response.status_code == 200

    created_booking = create_response.json()

    assert "bookingid" in created_booking
    assert isinstance(created_booking["bookingid"], int)

    booking_id = created_booking["bookingid"]

    # Act: filter bookings using the unique names.
    params = {
        "firstname": firstname,
        "lastname": lastname,
    }

    filter_response = requests.get(
        BASE_URL + "/booking",
        params=params,
        timeout=DEFAULT_TIMEOUT,
    )

    print("Request URL:", filter_response.url)
    print("Filtered response:", filter_response.json())

    # Assert: validate the filtered response.
    assert filter_response.status_code == 200
    assert "application/json" in filter_response.headers["Content-Type"]

    filtered_bookings = filter_response.json()

    assert isinstance(filtered_bookings, list)
    assert len(filtered_bookings) > 0

    returned_booking_ids = []

    for booking in filtered_bookings:
        assert isinstance(booking, dict)
        assert "bookingid" in booking
        assert isinstance(booking["bookingid"], int)

        returned_booking_ids.append(booking["bookingid"])

    assert booking_id in returned_booking_ids