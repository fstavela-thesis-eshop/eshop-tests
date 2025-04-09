import logging
from uuid import uuid4

import pytest

from tests.helpers import AUTHENTICATED_ENDPOINTS
from tests.helpers import APIClient
from tests.helpers import gen_create_customer_data
from tests.helpers import gen_str
from tests.helpers import gen_username

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("method, endpoint", AUTHENTICATED_ENDPOINTS)
def test_api_no_auth(method: str, endpoint: str) -> None:
    api_client_no_auth = APIClient()
    if "{}" in endpoint:
        endpoint = endpoint.format(str(uuid4()))
    response = api_client_no_auth.request(method, endpoint)
    assert response.status_code == 401


@pytest.mark.parametrize("method, endpoint", AUTHENTICATED_ENDPOINTS)
def test_api_wrong_username(method: str, endpoint: str) -> None:
    api_client_no_auth = APIClient(username=gen_username(), password=gen_str())
    if "{}" in endpoint:
        endpoint = endpoint.format(str(uuid4()))
    response = api_client_no_auth.request(method, endpoint)
    assert response.status_code == 401


@pytest.mark.parametrize("method, endpoint", AUTHENTICATED_ENDPOINTS)
def test_api_wrong_password(method: str, endpoint: str) -> None:
    api_client_no_auth = APIClient(username="admin", password=gen_str())
    if "{}" in endpoint:
        endpoint = endpoint.format(str(uuid4()))
    response = api_client_no_auth.request(method, endpoint)
    assert response.status_code == 401


@pytest.mark.parametrize(
    "method, endpoint", AUTHENTICATED_ENDPOINTS + (("POST", "/users/customers/create"),)
)
def test_api_correct_auth_admin(
    api_admin: APIClient, method: str, endpoint: str
) -> None:
    if "{}" in endpoint:
        endpoint = endpoint.format(str(uuid4()))
    response = api_admin.request(method, endpoint)
    assert response.status_code != 401


@pytest.mark.parametrize(
    "method, endpoint", AUTHENTICATED_ENDPOINTS + (("POST", "/users/customers/create"),)
)
def test_api_correct_auth_non_admin(
    api_customer: APIClient, method: str, endpoint: str
) -> None:
    if "{}" in endpoint:
        endpoint = endpoint.format(str(uuid4()))
    response = api_customer.request(method, endpoint)
    assert response.status_code != 401


def test_api_create_customers_no_auth() -> None:
    api_client = APIClient()
    response = api_client.post(
        "/users/customers/create", json=gen_create_customer_data()
    )
    assert response.status_code == 201


def test_api_auth_endpoint(api_admin: APIClient, api_customer: APIClient) -> None:
    admin_response = api_admin.get("/users/auth")
    assert admin_response.status_code == 200
    assert admin_response.json()["is_admin"] is True

    customer_response = api_customer.get("/users/auth")
    assert customer_response.status_code == 200
    assert customer_response.json()["is_admin"] is False


@pytest.mark.parametrize("include_id", (True, False))
def test_api_auth_headers_are_ignored(
    api_customer: APIClient, default_customer_id: str, admin_id: str, include_id: bool
) -> None:
    headers = {"x-is-admin": "true"}
    if include_id:
        headers["x-customer-id"] = admin_id

    response = api_customer.get("/users/auth", headers=headers)
    assert response.status_code == 200
    assert response.json()["is_admin"] is False
    assert response.json()["id"] == default_customer_id

    response = api_customer.get("/users/admins", headers=headers)
    assert response.status_code == 403
