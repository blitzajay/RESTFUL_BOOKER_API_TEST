from uuid import uuid4
import requests

BASE_URL = "https://restful-booker.herokuapp.com"


def test_delete_booking(auth_token):
    unique_value = uuid4().hex[:8]
    booking_payload = {
        "firstname": f"Ajay{unique_value}",
        "lastname": f"Kumar{unique_value}",
        "totalprice": 600,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-12-01",
            "checkout": "2026-12-05",
        },
        "additionalneeds": "Breakfast",
    }

    # Create a booking

    create_booking_response = requests.post(f"{BASE_URL}/booking", json= booking_payload, timeout=10)

    assert create_booking_response.status_code == 200

    booking_id = create_booking_response.json()["bookingid"]

    #Checking whether the booking exists first
    response_before_deleting = requests.get(f"{BASE_URL}/booking/{booking_id}", timeout=10)
    assert response_before_deleting.status_code == 200


    #Delete the booking

    delete_response = requests.delete(f"{BASE_URL}/booking/{booking_id}", cookies={"token":auth_token}, timeout=10)
    print("Delete status : ", delete_response.status_code)
    print("Delete response : ", delete_response.text)

    assert delete_response.status_code == 201

    # Hitting same id and checking whether the record doesnt exist now

    response_after_deleting = requests.get(f"{BASE_URL}/booking/{booking_id}", timeout=10)

    print(response_after_deleting.status_code)

    assert response_after_deleting.status_code == 404



