from tests.helpers import APIClient
from tests.helpers import gen_create_product_data


def test_api_create_product(
    api_admin: APIClient, prepare_category: dict[str, str]
) -> None:
    product_data = gen_create_product_data(prepare_category["id"])
    response = api_admin.post("/inventory/products/create", json=product_data)
    assert response.status_code == 201
    product_id = response.json()["id"]

    response = api_admin.get(f"/inventory/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == product_data["name"]

    response = api_admin.get("/inventory/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
    assert any(product["id"] == product_id for product in response.json())


def test_api_update_product(
    api_admin: APIClient, prepare_temporary_product: dict[str, str | int | float]
) -> None:
    response = api_admin.patch(
        f"/inventory/products/update/{prepare_temporary_product['id']}",
        json={"price": 99.9},
    )
    assert response.status_code == 200
    assert response.json()["price"] == 99.9

    response = api_admin.get(f"/inventory/products/{prepare_temporary_product['id']}")
    assert response.status_code == 200
    assert response.json()["price"] == 99.9


def test_api_product_change_stock_quantity(
    api_admin: APIClient, prepare_temporary_product: dict[str, str | int | float]
) -> None:
    update_data = [{"id": prepare_temporary_product["id"], "stock_quantity_dif": -10}]
    response = api_admin.patch("/inventory/products/stock", json=update_data)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert (
        response.json()[0]["stock_quantity"]
        == prepare_temporary_product["stock_quantity"] - 10  # type: ignore[operator]
    )

    response = api_admin.get(f"/inventory/products/{prepare_temporary_product['id']}")
    assert response.status_code == 200
    assert (
        response.json()["stock_quantity"]
        == prepare_temporary_product["stock_quantity"] - 10  # type: ignore[operator]
    )


def test_api_delete_product(
    api_admin: APIClient, prepare_temporary_product: dict[str, str | int | float]
) -> None:
    response = api_admin.delete(
        f"/inventory/products/{prepare_temporary_product['id']}"
    )
    assert response.status_code == 204

    response = api_admin.get(f"/inventory/products/{prepare_temporary_product['id']}")
    assert response.status_code == 404
