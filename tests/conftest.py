import pytest

from tests.helpers import APIClient
from tests.helpers import gen_create_category_data
from tests.helpers import gen_create_customer_data
from tests.helpers import gen_create_order_data
from tests.helpers import gen_create_product_data
from tests.helpers import gen_str
from tests.helpers import gen_username


@pytest.fixture(scope="session")
def api_admin() -> APIClient:
    return APIClient("admin", "admin")


@pytest.fixture(scope="session")
def admin_id(api_admin: APIClient) -> str:
    return api_admin.get("/users/auth").json()["id"]


@pytest.fixture(scope="session")
def api_customer(api_admin: APIClient) -> APIClient:
    username = gen_username()
    password = gen_str()
    api_admin.post(
        "/users/customers/create", json=gen_create_customer_data(username, password)
    )
    return APIClient(username, password)


@pytest.fixture(scope="session")
def default_customer_id(api_customer: APIClient) -> str:
    return api_customer.get("/users/auth").json()["id"]


@pytest.fixture()
def api_temporary_customer(api_admin: APIClient) -> APIClient:
    username = gen_username()
    password = gen_str()
    api_admin.post(
        "/users/customers/create", json=gen_create_customer_data(username, password)
    )
    return APIClient(username, password)


@pytest.fixture(scope="session")
def prepare_category(api_admin: APIClient) -> dict[str, str]:
    return api_admin.post(
        "/inventory/categories/create", json=gen_create_category_data()
    ).json()


@pytest.fixture()
def prepare_temporary_category(api_admin: APIClient) -> dict[str, str]:
    return api_admin.post(
        "/inventory/categories/create", json=gen_create_category_data()
    ).json()


@pytest.fixture(scope="session")
def prepare_product(
    api_admin: APIClient, prepare_category: dict[str, str]
) -> dict[str, str | int | float]:
    return api_admin.post(
        "/inventory/products/create",
        json=gen_create_product_data(prepare_category["id"]),
    ).json()


@pytest.fixture()
def prepare_temporary_product(
    api_admin: APIClient, prepare_temporary_category: dict[str, str]
) -> dict[str, str | int | float]:
    return api_admin.post(
        "/inventory/products/create",
        json=gen_create_product_data(prepare_temporary_category["id"]),
    ).json()


@pytest.fixture()
def prepare_temporary_order(
    api_customer: APIClient,
    default_customer_id: str,
    prepare_temporary_product: dict[str, str | int | float],
) -> dict[str, str | int | list[dict[str, str | int | float]]]:
    return api_customer.post(
        "/orders/orders/create",
        json=gen_create_order_data(
            default_customer_id,
            [prepare_temporary_product["id"]],  # type: ignore[list-item]
        ),
    ).json()
