import pytest
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient

pytestmark = pytest.mark.anyio


async def test_health(client: AsyncTestClient) -> None:
    response = await client.get("/health")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"status": "ok"}


async def test_openapi_schema_available(client: AsyncTestClient) -> None:
    response = await client.get("/schema/openapi.json")
    assert response.status_code == HTTP_200_OK
    schema = response.json()
    assert schema["info"]["title"] == "Todo API"
    assert "/health" not in schema["paths"]
