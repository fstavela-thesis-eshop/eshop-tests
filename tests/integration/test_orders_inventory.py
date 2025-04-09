import logging

from tests.helpers import APIClient
from tests.helpers import gen_create_order_data

logger = logging.getLogger(__name__)


def test_create_order_changes_product_stock_quantity(
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

    response = api_customer.get(
        f"/inventory/products/{prepare_temporary_product['id']}"
    )
    assert response.status_code == 200
    assert (
        response.json()["stock_quantity"]
        == prepare_temporary_product["stock_quantity"]  # type: ignore[operator]
        - create_data["items"][0]["quantity"]  # type: ignore[index]
    )


def test_cancel_order_changes_product_stock_quantity(
    api_customer: APIClient,
    prepare_temporary_order: dict[str, str | int | list[dict[str, str | int | float]]],
) -> None:
    product_id = prepare_temporary_order["items"][0]["product_id"]  # type: ignore[index]
    response = api_customer.get(f"/inventory/products/{product_id}")
    assert response.status_code == 200
    initial_stock_quantity = response.json()["stock_quantity"]

    response = api_customer.delete(
        f"/orders/orders/{prepare_temporary_order['order_id']}"
    )
    assert response.status_code == 200

    response = api_customer.get(f"/inventory/products/{product_id}")
    assert response.status_code == 200
    assert (
        response.json()["stock_quantity"]
        == initial_stock_quantity + prepare_temporary_order["items"][0]["quantity"]  # type: ignore[index]
    )


def test_create_order_not_enough_stock_quantity(
    api_customer: APIClient,
    default_customer_id: str,
    prepare_temporary_product: dict[str, str | int | float],
) -> None:
    create_data = gen_create_order_data(
        default_customer_id,
        [prepare_temporary_product["id"]],  # type: ignore[list-item]
        quantity=500,
    )
    response = api_customer.post("/orders/orders/create", json=create_data)
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == f"Not enough product in stock: {prepare_temporary_product['id']}"
    )
