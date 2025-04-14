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
