import pytest

from helpers.api_helpers import APIClient


@pytest.fixture(scope="session")
def api_admin() -> APIClient:
    return APIClient("admin", "admin")
