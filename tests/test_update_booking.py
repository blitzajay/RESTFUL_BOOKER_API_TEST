from uuid import uuid4

import requests


from config.settings import BASE_URL, DEFAULT_TIMEOUT


def test_update_complete_booking(auth_token):
    unique_value = uuid4().hex[:8]

    original_payload = {
        "firstname": f"Ajay{unique_value}",
        "lastname": f"Kumar{unique_value}",
        "totalprice": 500,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2026-10-01",
            "checkout": "2026-10-05",
        },
        "additionalneeds": "Breakfast",
    }

    # Arrange: create a booking.
    create_response = requests.post(
        BASE_URL + "/booking",
        json=original_payload,
        timeout=DEFAULT_TIMEOUT,
    )

    assert create_response.status_code == 200

    booking_id = create_response.json()["bookingid"]

    updated_payload = {
        "firstname": f"Updated{unique_value}",
        "lastname": f"Booking{unique_value}",
        "totalprice": 900,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-11-01",
            "checkout": "2026-11-10",
        },
        "additionalneeds": "Late checkout",
    }

    # Act: completely replace the booking.
    update_response = requests.put(
        f"{BASE_URL}/booking/{booking_id}",
        json=updated_payload,
        cookies={"token": auth_token},
        headers={"Accept": "application/json"},
        timeout=DEFAULT_TIMEOUT,
    )

    print("Update response:", update_response.json())

    # Assert the update response.
    assert update_response.status_code == 200
    assert "application/json" in update_response.headers["Content-Type"]
    assert update_response.json() == updated_payload

    # Verify the persisted booking.
    get_response = requests.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=DEFAULT_TIMEOUT,
    )

    assert get_response.status_code == 200
    assert get_response.json() == updated_payload