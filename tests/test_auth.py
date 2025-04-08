import logging

from helpers.api_helpers import APIClient

logger = logging.getLogger(__name__)


def test_api_get(api_admin: APIClient) -> None:
    response = api_admin.get("/users/customers")
    logger.info(response.json())
