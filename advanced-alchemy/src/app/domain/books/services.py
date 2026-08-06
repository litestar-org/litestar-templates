from advanced_alchemy.extensions.litestar import repository, service

from app.db.models import Book


class BookService(service.SQLAlchemyAsyncRepositoryService[Book]):
    """Data access and domain logic for books."""

    class Repo(repository.SQLAlchemyAsyncRepository[Book]):
        model_type = Book

    repository_type = Repo
