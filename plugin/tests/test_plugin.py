import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND
from litestar.testing import AsyncTestClient

from litestar_example_plugin import HealthCheckConfig, HealthCheckPlugin

pytestmark = pytest.mark.anyio


async def test_plugin_registers_default_route() -> None:
    app = Litestar(plugins=[HealthCheckPlugin()])
    async with AsyncTestClient(app=app) as client:
        response = await client.get("/health")
        assert response.status_code == HTTP_200_OK
        assert response.json() == {"status": "ok"}


async def test_plugin_respects_custom_path() -> None:
    plugin = HealthCheckPlugin(HealthCheckConfig(path="/livez"))
    app = Litestar(plugins=[plugin])
    async with AsyncTestClient(app=app) as client:
        assert (await client.get("/livez")).status_code == HTTP_200_OK
        assert (await client.get("/health")).status_code == HTTP_404_NOT_FOUND


async def test_route_is_hidden_from_schema_by_default() -> None:
    app = Litestar(plugins=[HealthCheckPlugin()])
    async with AsyncTestClient(app=app) as client:
        schema = (await client.get("/schema/openapi.json")).json()
        assert "/health" not in schema["paths"]
