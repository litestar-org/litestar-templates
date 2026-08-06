from collections.abc import AsyncIterator

import pytest
from litestar.testing import AsyncTestClient

from app import app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> AsyncIterator[AsyncTestClient]:
    async with AsyncTestClient(app=app) as client:
        yield client
