from clients.base_client import BaseClient


class BookingClient(BaseClient):

    def get_all_bookings(self, params=None):
        return self.request(
            "GET",
            "/booking",
            params=params,
        )

    def get_booking(self, booking_id):
        return self.request(
            "GET",
            f"/booking/{booking_id}",
        )

    def create_booking(self, payload):
        return self.request(
            "POST",
            "/booking",
            json=payload,
            headers={"Accept": "application/json"},
        )

    def update_booking(self, booking_id, payload, auth_token):
        return self.request(
            "PUT",
            f"/booking/{booking_id}",
            json=payload,
            cookies={"token": auth_token},
            headers={"Accept": "application/json"},
        )

    def partial_update_booking(self, booking_id, payload, auth_token):
        return self.request(
            "PATCH",
            f"/booking/{booking_id}",
            json=payload,
            cookies={"token": auth_token},
            headers={"Accept": "application/json"},
        )

    def delete_booking(self, booking_id, auth_token):
        return self.request(
            "DELETE",
            f"/booking/{booking_id}",
            cookies={"token": auth_token},
        )
