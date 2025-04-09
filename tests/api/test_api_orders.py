from tests.helpers import APIClient
from tests.helpers import gen_create_order_data


def test_api_create_order(
    api_customer: APIClient,
    default_customer_id: str,
    prepare_temporary_product: dict[str, str | int | float],
) -> None:
    create_data = gen_create_order_data(
        default_customer_id,
        [prepare_temporary_product["id"]],  # type: ignore[list-item]
    )
    response = api_customer.post("/orders/orders/create", json=create_data)
    assert response.status_code == 201
    json_response = response.json()
    order_id = json_response["order_id"]
    assert json_response["customer_id"] == default_customer_id
    assert isinstance(json_response["items"], list)
    assert len(json_response["items"]) == 1
    assert json_response["items"][0]["product_id"] == prepare_temporary_product["id"]
    assert (
        json_response["total_price"]
        == prepare_temporary_product["price"] * create_data["items"][0]["quantity"]  # type: ignore[operator, index]
    )
    assert json_response["status"] == "created"
    assert json_response["created_at"] <= json_response["updated_at"]

    response = api_customer.get(f"/orders/orders/{order_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["order_id"] == order_id
    assert json_response["customer_id"] == default_customer_id
    assert json_response["created_at"] <= json_response["updated_at"]

    response = api_customer.get(f"/orders/orders/customer/{default_customer_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
    assert any(order["order_id"] == order_id for order in response.json())

    response = api_customer.get("/orders/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
    assert any(order["order_id"] == order_id for order in response.json())


def test_api_update_order_status(
    api_admin: APIClient,
    prepare_temporary_order: dict[str, str | int | list[dict[str, str | int | float]]],
) -> None:
    response = api_admin.patch(
        f"/orders/orders/{prepare_temporary_order['order_id']}",
        json={"status": "paid"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "paid"
    assert response.json()["created_at"] == prepare_temporary_order["created_at"]
    assert response.json()["updated_at"] > prepare_temporary_order["updated_at"]

    response = api_admin.get(f"/orders/orders/{prepare_temporary_order['order_id']}")
    assert response.status_code == 200
    assert response.json()["status"] == "paid"
    assert response.json()["created_at"] == prepare_temporary_order["created_at"]
    assert response.json()["updated_at"] > prepare_temporary_order["updated_at"]


def test_api_cancel_order(
    api_admin: APIClient,
    prepare_temporary_order: dict[str, str | int | list[dict[str, str | int | float]]],
) -> None:
    response = api_admin.delete(f"/orders/orders/{prepare_temporary_order['order_id']}")
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"
    assert response.json()["created_at"] == prepare_temporary_order["created_at"]
    assert response.json()["updated_at"] > prepare_temporary_order["updated_at"]

    response = api_admin.get(f"/orders/orders/{prepare_temporary_order['order_id']}")
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"
    assert response.json()["created_at"] == prepare_temporary_order["created_at"]
    assert response.json()["updated_at"] > prepare_temporary_order["updated_at"]
