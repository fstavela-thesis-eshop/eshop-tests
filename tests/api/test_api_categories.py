from tests.helpers import APIClient
from tests.helpers import gen_create_category_data


def test_api_create_category(api_admin: APIClient) -> None:
    create_data = gen_create_category_data()
    response = api_admin.post("/inventory/categories/create", json=create_data)
    assert response.status_code == 201
    assert response.json()["name"] == create_data["name"]
    category_id = response.json()["id"]

    response = api_admin.get(f"/inventory/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["name"] == create_data["name"]

    response = api_admin.get("/inventory/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
    assert any(category["id"] == category_id for category in response.json())


def test_api_update_category(
    api_admin: APIClient, prepare_temporary_category: dict[str, str]
) -> None:
    response = api_admin.patch(
        f"/inventory/categories/{prepare_temporary_category['id']}",
        json={"description": "The best toys"},
    )
    assert response.status_code == 200
    assert response.json()["description"] == "The best toys"

    response = api_admin.get(
        f"/inventory/categories/{prepare_temporary_category['id']}"
    )
    assert response.status_code == 200
    assert response.json()["description"] == "The best toys"


def test_api_delete_category(
    api_admin: APIClient, prepare_temporary_category: dict[str, str]
) -> None:
    response = api_admin.delete(
        f"/inventory/categories/{prepare_temporary_category['id']}"
    )
    assert response.status_code == 204

    response = api_admin.get(
        f"/inventory/categories/{prepare_temporary_category['id']}"
    )
    assert response.status_code == 404
