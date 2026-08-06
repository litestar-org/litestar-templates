"""Database CRUD with Advanced Alchemy's repository/service layer.

- ``Book`` is a SQLAlchemy model on ``UUIDAuditBase`` (UUID PK plus
  ``created_at``/``updated_at`` audit columns).
- ``BookService`` wraps a typed async repository — services own data access;
  handlers stay thin.
- ``SQLAlchemyPlugin`` manages the engine, sessions, and per-request
  transactions (autocommit on success).

SQLite is used so the starter runs with zero setup; swap ``DATABASE_URL`` for
PostgreSQL (``postgresql+asyncpg://...``) when you're ready.
"""

import os
from collections.abc import AsyncIterator
from uuid import UUID

import msgspec
from advanced_alchemy.exceptions import NotFoundError
from advanced_alchemy.extensions.litestar import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyDTO,
    SQLAlchemyPlugin,
    base,
    repository,
    service,
)
from litestar import Controller, Litestar, Request, Response, delete, get, post
from litestar.di import NamedDependency, Provide
from litestar.params import FromPath
from litestar.status_codes import HTTP_404_NOT_FOUND
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3")


class Book(base.UUIDAuditBase):
    """A book. UUID primary key and audit timestamps come from the base."""

    __tablename__ = "book"

    title: Mapped[str]
    author: Mapped[str]


class BookCreate(msgspec.Struct):
    """Payload for creating a book."""

    title: str
    author: str


class BookService(service.SQLAlchemyAsyncRepositoryService[Book]):
    """Data access for books. Add domain logic here, not in handlers."""

    class Repo(repository.SQLAlchemyAsyncRepository[Book]):
        model_type = Book

    repository_type = Repo


async def provide_books_service(
    db_session: NamedDependency[AsyncSession],
) -> AsyncIterator[BookService]:
    async with BookService.new(session=db_session) as books_service:
        yield books_service


class BookController(Controller):
    """CRUD endpoints for books."""

    path = "/books"
    tags = ["books"]
    dependencies = {"books_service": Provide(provide_books_service)}
    return_dto = SQLAlchemyDTO[Book]

    @get("/")
    async def list_books(
        self, books_service: NamedDependency[BookService]
    ) -> list[Book]:
        return list(await books_service.get_many())

    @get("/{book_id:uuid}")
    async def get_book(
        self, books_service: NamedDependency[BookService], book_id: FromPath[UUID]
    ) -> Book:
        return await books_service.get(book_id)

    @post("/")
    async def create_book(
        self, books_service: NamedDependency[BookService], data: BookCreate
    ) -> Book:
        return await books_service.create(msgspec.structs.asdict(data))

    @delete("/{book_id:uuid}")
    async def delete_book(
        self, books_service: NamedDependency[BookService], book_id: FromPath[UUID]
    ) -> None:
        await books_service.delete(book_id)


def not_found_handler(request: Request, exc: NotFoundError) -> Response[dict[str, str]]:
    return Response(
        status_code=HTTP_404_NOT_FOUND,
        content={"detail": str(exc) or "Not found"},
    )


def create_app(database_url: str = DATABASE_URL) -> Litestar:
    """App factory — lets tests inject their own database URL."""
    db_config = SQLAlchemyAsyncConfig(
        connection_string=database_url,
        create_all=True,
        # Commit on 2xx responses, roll back otherwise (and on exceptions).
        before_send_handler="autocommit",
    )
    return Litestar(
        route_handlers=[BookController],
        plugins=[SQLAlchemyPlugin(config=db_config)],
        exception_handlers={NotFoundError: not_found_handler},
    )


app = create_app()
