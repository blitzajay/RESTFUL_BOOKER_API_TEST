from clients.base_client import BaseClient


class AuthClient(BaseClient):

    def create_token(self, payload):
        return self.request(
            "POST",
            "/auth",
            json=payload,
            headers={"Accept": "application/json"},
        )
