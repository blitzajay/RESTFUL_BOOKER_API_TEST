import requests

BASE_URL = "https://restful-booker.herokuapp.com"

def test_get_all_booking_ids():
    # response = requests.get(f"{BASE_URL}/booking", timeout=10)
    response = requests.get(BASE_URL+"/booking", timeout=10)

    # print(response.json())

    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, list)
    assert len(body) > 0

    for booking in body:
        assert isinstance(booking, dict)
        assert "bookingid" in booking
        assert isinstance(booking["bookingid"], int)
        assert booking["bookingid"] > 0


    assert "application/json" in response.headers["Content-Type"]

    assert response.elapsed.total_seconds() < 5

