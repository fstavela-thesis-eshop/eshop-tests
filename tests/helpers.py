from random import choices
from random import randint
from string import ascii_letters
from string import digits
from string import punctuation
from typing import Any

from requests import Response
from requests import Session

AUTHENTICATED_ENDPOINTS = (
    ("GET", "/users/customers"),
    ("GET", "/users/customers/{}"),
    ("PATCH", "/users/customers/{}"),
    ("GET", "/users/auth"),
    ("GET", "/users/admins"),
    ("PUT", "/users/admins/{}"),
    ("DELETE", "/users/admins/{}"),
    ("GET", "/inventory/products"),
    ("GET", "/inventory/products/{}"),
    ("DELETE", "/inventory/products/{}"),
    ("POST", "/inventory/products/create"),
    ("PATCH", "/inventory/products/update/{}"),
    ("PATCH", "/inventory/products/stock"),
    ("GET", "/inventory/categories"),
    ("GET", "/inventory/categories/{}"),
    ("PATCH", "/inventory/categories/{}"),
    ("DELETE", "/inventory/categories/{}"),
    ("POST", "/inventory/categories/create"),
    ("GET", "/orders/orders"),
    ("GET", "/orders/orders/customer/{}"),
    ("GET", "/orders/orders/{}"),
    ("PATCH", "/orders/orders/{}"),
    ("DELETE", "/orders/orders/{}"),
    ("POST", "/orders/orders/create"),
    ("GET", "/notifications/notifications"),
    ("GET", "/notifications/notifications/{}"),
)


class APIClient:
    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        base_url: str = "http://localhost:8080",
    ):
        self.base_url = base_url
        self.session = Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.session.headers.update({"Accept": "application/json"})
        if username and password:
            self.session.auth = (username, password)

    def request(
        self, method: str, endpoint: str, *args: Any, **kwargs: Any
    ) -> Response:
        return self.session.request(method, self.base_url + endpoint, *args, **kwargs)

    def get(self, endpoint: str, *args: Any, **kwargs: Any) -> Response:
        return self.request("GET", endpoint, *args, **kwargs)

    def post(self, endpoint: str, *args: Any, **kwargs: Any) -> Response:
        return self.request("POST", endpoint, *args, **kwargs)

    def patch(self, endpoint: str, *args: Any, **kwargs: Any) -> Response:
        return self.request("PATCH", endpoint, *args, **kwargs)

    def put(self, endpoint: str, *args: Any, **kwargs: Any) -> Response:
        return self.request("PUT", endpoint, *args, **kwargs)

    def delete(self, endpoint: str, *args: Any, **kwargs: Any) -> Response:
        return self.request("DELETE", endpoint, *args, **kwargs)


def gen_str(
    length: int = 10,
    *,
    use_letters: bool = True,
    use_digits: bool = True,
    use_punctuation: bool = True,
) -> str:
    symbols = ""
    if use_letters:
        symbols += ascii_letters
    if use_digits:
        symbols += digits
    if use_punctuation:
        symbols += punctuation
    return "".join(choices(symbols, k=length))


def gen_username(length: int = 10) -> str:
    return gen_str(length=length, use_punctuation=False)


def gen_create_customer_data(
    username: str | None = None, password: str | None = None, email: str | None = None
) -> dict[str, str]:
    username = username or gen_username()
    return {
        "username": username,
        "password": password or gen_str(),
        "first_name": gen_str(use_digits=False, use_punctuation=False)
        .lower()
        .capitalize(),
        "last_name": gen_str(use_digits=False, use_punctuation=False)
        .lower()
        .capitalize(),
        "email": email or f"{username}@example.com",
        "address": gen_str(50, use_punctuation=False),
        "phone": f"{gen_str(9, use_letters=False, use_punctuation=False)}",
    }


def gen_create_product_data(
    category_id: str, in_stock: bool = True
) -> dict[str, str | int]:
    return {
        "name": gen_str(use_digits=False, use_punctuation=False),
        "description": gen_str(50, use_digits=False, use_punctuation=False),
        "category_id": category_id,
        "price": randint(10, 5000),
        "stock_quantity": randint(10, 100) if in_stock else 0,
    }


def gen_create_category_data() -> dict[str, str]:
    return {
        "name": gen_str(use_digits=False, use_punctuation=False),
        "description": gen_str(50, use_digits=False, use_punctuation=False),
    }


def gen_create_order_data(
    customer_id: str, product_ids: list[str], quantity: int | None = None
) -> dict[str, str | list[dict[str, str | int]]]:
    return {
        "customer_id": customer_id,
        "items": [
            {"product_id": product_id, "quantity": quantity or randint(1, 10)}
            for product_id in product_ids
        ],
    }
