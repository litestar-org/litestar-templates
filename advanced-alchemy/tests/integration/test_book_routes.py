import pytest
from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)
from litestar.testing import AsyncTestClient

pytestmark = pytest.mark.anyio


async def test_crud_roundtrip(client: AsyncTestClient) -> None:
    created = await client.post(
        "/books", json={"title": "The Pragmatic Programmer", "author": "Hunt & Thomas"}
    )
    assert created.status_code == HTTP_201_CREATED
    book = created.json()
    assert book["title"] == "The Pragmatic Programmer"
    assert "id" in book and "created_at" in book

    listed = await client.get("/books")
    assert listed.status_code == HTTP_200_OK
    assert len(listed.json()) == 1

    fetched = await client.get(f"/books/{book['id']}")
    assert fetched.status_code == HTTP_200_OK
    assert fetched.json()["author"] == "Hunt & Thomas"

    deleted = await client.delete(f"/books/{book['id']}")
    assert deleted.status_code == HTTP_204_NO_CONTENT

    assert (await client.get("/books")).json() == []


async def test_missing_book_returns_404(client: AsyncTestClient) -> None:
    response = await client.get("/books/00000000-0000-0000-0000-000000000000")
    assert response.status_code == HTTP_404_NOT_FOUND
