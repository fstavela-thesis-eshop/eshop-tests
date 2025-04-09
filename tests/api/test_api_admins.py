from tests.helpers import APIClient


def test_api_add_admin(api_admin: APIClient, api_temporary_customer: APIClient) -> None:
    customer_id = api_temporary_customer.get("/users/auth").json()["id"]
    response = api_admin.put(f"/users/admins/{customer_id}")
    assert response.status_code == 204

    response = api_temporary_customer.get("/users/admins")
    assert response.status_code == 200
    assert customer_id in response.json()

    response = api_temporary_customer.get("/users/auth")
    assert response.json()["is_admin"] is True


def test_api_remove_admin(
    api_admin: APIClient, api_temporary_customer: APIClient
) -> None:
    customer_id = api_temporary_customer.get("/users/auth").json()["id"]
    api_admin.put(f"/users/admins/{customer_id}")

    response = api_admin.delete(f"/users/admins/{customer_id}")
    assert response.status_code == 204

    response = api_admin.get("/users/admins")
    assert response.status_code == 200
    assert customer_id not in response.json()

    response = api_temporary_customer.get("/users/auth")
    assert response.json()["is_admin"] is False
