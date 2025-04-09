from time import sleep

from tests.helpers import APIClient
from tests.helpers import gen_create_order_data


def test_create_order_triggers_notification(
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
    order_id = response.json()["order_id"]

    sleep(1)  # Orders -> notifications communication is async, so it's not instant

    response = api_customer.get("/notifications/notifications")
    assert response.status_code == 200
    json_response = response.json()
    assert isinstance(json_response, list)
    assert len(json_response) >= 1
    assert json_response[-1]["customer_id"] == default_customer_id
    assert json_response[-1]["message"] == f"Order {order_id} was successfully created."

    response = api_customer.get(f"/notifications/notifications/{default_customer_id}")
    assert response.status_code == 200
    assert response.json() == json_response


def test_update_order_status_triggers_notification(
    api_admin: APIClient,
    prepare_temporary_order: dict[str, str | int | list[dict[str, str | int | float]]],
) -> None:
    response = api_admin.patch(
        f"/orders/orders/{prepare_temporary_order['order_id']}",
        json={"status": "paid"},
    )
    assert response.status_code == 200

    sleep(1)  # Orders -> notifications communication is async, so it's not instant

    response = api_admin.get("/notifications/notifications")
    assert response.status_code == 200
    json_response = response.json()
    assert isinstance(json_response, list)
    assert len(json_response) >= 1
    assert (
        json_response[-1]["message"]
        == f"Order {prepare_temporary_order['order_id']} was paid. Thank you!"
    )


def test_cancel_order_triggers_notification(
    api_admin: APIClient,
    prepare_temporary_order: dict[str, str | int | list[dict[str, str | int | float]]],
) -> None:
    response = api_admin.delete(f"/orders/orders/{prepare_temporary_order['order_id']}")
    assert response.status_code == 200

    sleep(1)  # Orders -> notifications communication is async, so it's not instant

    response = api_admin.get("/notifications/notifications")
    assert response.status_code == 200
    json_response = response.json()
    assert isinstance(json_response, list)
    assert len(json_response) >= 1
    assert (
        json_response[-1]["message"]
        == f"Order {prepare_temporary_order['order_id']} was cancelled."
    )
