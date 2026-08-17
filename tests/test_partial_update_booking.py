from uuid import uuid4
import requests

from config.settings import BASE_URL, DEFAULT_TIMEOUT

def test_partial_update_booking(auth_token):
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

    create_response = requests.post(
        BASE_URL + "/booking",
        json=original_payload,
        timeout=DEFAULT_TIMEOUT,
    )

    assert create_response.status_code == 200

    booking_id = create_response.json()["bookingid"]

    # Only these fields should change.
    partial_payload = {
        "totalprice": 950,
        "depositpaid": True,
        "additionalneeds": "Late checkout",
    }

    # Act: partially update the booking.
    patch_response = requests.patch(
        f"{BASE_URL}/booking/{booking_id}",
        json=partial_payload,
        cookies={"token": auth_token},
        headers={"Accept": "application/json"},
        timeout=DEFAULT_TIMEOUT,
    )

    assert patch_response.status_code == 200
    assert "application/json" in patch_response.headers["Content-Type"]

    updated_booking = patch_response.json()

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
    get_response = requests.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=DEFAULT_TIMEOUT,
    )

    assert get_response.status_code == 200
    assert get_response.json() == updated_booking













