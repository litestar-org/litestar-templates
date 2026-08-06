"""Dependency providers for the books domain."""

from collections.abc import AsyncIterator

from litestar.di import NamedDependency
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.books.services import BookService


async def provide_books_service(
    db_session: NamedDependency[AsyncSession],
) -> AsyncIterator[BookService]:
    """Build a request-scoped service on the plugin-managed session."""
    async with BookService.new(session=db_session) as books_service:
        yield books_service
