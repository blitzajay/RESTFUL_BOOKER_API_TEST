from uuid import uuid4

def create_booking_payload(**overrides):
    unique_value = uuid4().hex[:8]

    payload = {
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

    payload.update(overrides)

    return payload
