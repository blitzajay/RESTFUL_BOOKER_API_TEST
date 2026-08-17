from uuid import uuid4

import requests


BASE_URL = "https://restful-booker.herokuapp.com"


def test_create_booking():
    unique_value = uuid4().hex[:8]

    booking_payload = {
        "firstname": f"Ajay{unique_value}",
        "lastname": f"Kumar{unique_value}",
        "totalprice": 750,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-10-01",
            "checkout": "2026-10-05",
        },
        "additionalneeds": "Breakfast",
    }

    create_response = requests.post(
        BASE_URL + "/booking",
        json=booking_payload,
        headers={"Accept": "application/json"},
        timeout=10,
    )

    assert create_response.status_code == 200
    assert "application/json" in create_response.headers["Content-Type"]

    response_body = create_response.json()

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

    get_response = requests.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=10,
    )

    assert get_response.status_code == 200
    assert get_response.json() == booking_payload