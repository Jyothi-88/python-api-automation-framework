import requests


class OrderApiClient:
    """Reusable HTTP client for REST API automation."""

    def __init__(self, base_url: str, token: str, session=None):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
        })

        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def create_order(self, order_data: dict):
        return self.session.post(
            f"{self.base_url}/orders",
            json=order_data,
        )

    def get_order(self, order_id: str):
        return self.session.get(
            f"{self.base_url}/orders/{order_id}",
        )

    def update_order_status(self, order_id: str, status: str):
        return self.session.patch(
            f"{self.base_url}/orders/{order_id}",
            json={"status": status},
        )

    def delete_order(self, order_id: str):
        return self.session.delete(
            f"{self.base_url}/orders/{order_id}",
        )