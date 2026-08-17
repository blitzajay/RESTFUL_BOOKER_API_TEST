import pytest

from factories.booking_factory import create_booking_payload
from utils.response_validators import assert_status_code


@pytest.mark.regression
@pytest.mark.booking
def test_delete_booking(booking_client, auth_token):
    booking_payload = create_booking_payload(
        totalprice=600,
        depositpaid=True,
    )

    # Create a booking

    create_booking_response = booking_client.create_booking(booking_payload)

    assert_status_code(create_booking_response, 200)

    booking_id = create_booking_response.json()["bookingid"]

    #Checking whether the booking exists first
    response_before_deleting = booking_client.get_booking(booking_id)
    assert_status_code(response_before_deleting, 200)


    #Delete the booking

    delete_response = booking_client.delete_booking(booking_id, auth_token)
    print("Delete status : ", delete_response.status_code)
    print("Delete response : ", delete_response.text)

    assert_status_code(delete_response, 201)

    # Hitting same id and checking whether the record doesnt exist now

    response_after_deleting = booking_client.get_booking(booking_id)

    print(response_after_deleting.status_code)

    assert_status_code(response_after_deleting, 404)
