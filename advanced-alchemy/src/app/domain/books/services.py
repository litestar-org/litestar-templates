"""Business logic for the books domain.

The service wraps a typed async repository — data access lives here, not in
controllers. Add domain rules as methods or lifecycle hooks
(``to_model_on_create`` etc.).
"""

from advanced_alchemy.extensions.litestar import repository, service

from app.db.models import Book


class BookService(service.SQLAlchemyAsyncRepositoryService[Book]):
    """Data access and domain logic for books."""

    class Repo(repository.SQLAlchemyAsyncRepository[Book]):
        model_type = Book

    repository_type = Repo
