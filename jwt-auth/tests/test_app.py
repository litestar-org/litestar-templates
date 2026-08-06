import pytest
from litestar.status_codes import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from litestar.testing import AsyncTestClient

pytestmark = pytest.mark.anyio


async def login(client: AsyncTestClient) -> str:
    response = await client.post(
        "/login", json={"username": "admin", "password": "s3cret"}
    )
    assert response.status_code in (HTTP_200_OK, 201)
    return response.headers["Authorization"]


async def test_login_issues_token(client: AsyncTestClient) -> None:
    token = await login(client)
    assert token.startswith("Bearer ")


async def test_wrong_password_is_rejected(client: AsyncTestClient) -> None:
    response = await client.post(
        "/login", json={"username": "admin", "password": "nope"}
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED


async def test_protected_route_requires_token(client: AsyncTestClient) -> None:
    response = await client.get("/me")
    assert response.status_code == HTTP_401_UNAUTHORIZED


async def test_protected_route_with_token(client: AsyncTestClient) -> None:
    token = await login(client)
    response = await client.get("/me", headers={"Authorization": token})
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"id": "admin", "name": "Admin User"}
