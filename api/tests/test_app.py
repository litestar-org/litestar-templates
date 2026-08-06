import pytest
from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from litestar.testing import AsyncTestClient

pytestmark = pytest.mark.anyio


async def test_crud_roundtrip(client: AsyncTestClient) -> None:
    created = await client.post("/todos", json={"title": "write tests"})
    assert created.status_code == HTTP_201_CREATED
    todo = created.json()
    todo_id = todo["id"]
    assert todo["title"] == "write tests"
    assert todo["done"] is False

    listed = await client.get("/todos")
    assert listed.status_code == HTTP_200_OK
    assert any(item["id"] == todo_id for item in listed.json())

    updated = await client.put(
        f"/todos/{todo_id}", json={"title": "write tests", "done": True}
    )
    assert updated.status_code == HTTP_200_OK
    assert updated.json()["done"] is True

    deleted = await client.delete(f"/todos/{todo_id}")
    assert deleted.status_code == HTTP_204_NO_CONTENT

    missing = await client.get(f"/todos/{todo_id}")
    assert missing.status_code == HTTP_404_NOT_FOUND


async def test_validation_rejects_bad_payload(client: AsyncTestClient) -> None:
    response = await client.post("/todos", json={"done": True})
    assert response.status_code == HTTP_400_BAD_REQUEST


async def test_openapi_schema_available(client: AsyncTestClient) -> None:
    response = await client.get("/schema/openapi.json")
    assert response.status_code == HTTP_200_OK
    assert response.json()["info"]["title"] == "Todo API"
