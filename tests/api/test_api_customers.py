import logging

from tests.helpers import APIClient
from tests.helpers import gen_create_customer_data

logger = logging.getLogger(__name__)


def test_api_create_customer(api_admin: APIClient) -> None:
    create_customer_data = gen_create_customer_data()
    response = api_admin.post("/users/customers/create", json=create_customer_data)
    assert response.status_code == 201
    assert response.json()["username"] == create_customer_data["username"]
    customer_id = response.json()["id"]

    response = api_admin.get(f"/users/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["username"] == create_customer_data["username"]

    response = api_admin.get("/users/customers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2
    assert any(customer["id"] == customer_id for customer in response.json())


def test_api_update_customer(api_customer: APIClient, default_customer_id: str) -> None:
    update_customer_data = {"phone": "+420 123 456 789"}
    response = api_customer.patch(
        f"/users/customers/{default_customer_id}", json=update_customer_data
    )
    assert response.status_code == 200
    assert response.json()["phone"] == "+420 123 456 789"

    response = api_customer.get(f"/users/customers/{default_customer_id}")
    assert response.status_code == 200
    assert response.json()["phone"] == "+420 123 456 789"


def test_api_create_customer_with_same_username(
    api_admin: APIClient, api_temporary_customer: APIClient
) -> None:
    response = api_temporary_customer.get("/users/customers")
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)
    assert len(response_json) == 1

    create_customer_data = gen_create_customer_data(
        username=response_json[0]["username"]
    )
    response = api_admin.post("/users/customers/create", json=create_customer_data)
    assert response.status_code == 400


def test_api_create_customer_with_same_email(
    api_admin: APIClient, api_temporary_customer: APIClient
) -> None:
    response = api_temporary_customer.get("/users/customers")
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)
    assert len(response_json) == 1

    create_customer_data = gen_create_customer_data(email=response_json[0]["email"])
    response = api_admin.post("/users/customers/create", json=create_customer_data)
    assert response.status_code == 400
