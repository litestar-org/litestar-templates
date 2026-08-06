import pytest
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient

from app import app


@pytest.mark.anyio
async def test_index() -> None:
    async with AsyncTestClient(app=app) as client:
        response = await client.get("/")
        assert response.status_code == HTTP_200_OK
        assert response.json() == {"message": "Hello, Litestar!"}
