from collections.abc import AsyncIterator

import pytest
from litestar.testing import AsyncTestClient

from app.server.asgi import create_app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> AsyncIterator[AsyncTestClient]:
    async with AsyncTestClient(app=create_app()) as client:
        yield client
