import pytest
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient

pytestmark = pytest.mark.anyio


async def test_timing_header_is_added(client: AsyncTestClient) -> None:
    response = await client.get("/")
    assert response.status_code == HTTP_200_OK
    assert response.headers["X-Response-Time"].endswith("ms")


async def test_excluded_path_is_skipped(client: AsyncTestClient) -> None:
    response = await client.get("/schema/openapi.json")
    assert response.status_code == HTTP_200_OK
    assert "X-Response-Time" not in response.headers
