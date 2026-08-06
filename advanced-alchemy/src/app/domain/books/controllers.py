from uuid import UUID

import msgspec
from advanced_alchemy.extensions.litestar import SQLAlchemyDTO
from litestar import Controller, delete, get, post
from litestar.di import NamedDependency, Provide
from litestar.params import FromPath

from app.db.models import Book
from app.domain.books.deps import provide_books_service
from app.domain.books.schemas import BookCreate
from app.domain.books.services import BookService


class BookController(Controller):
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
