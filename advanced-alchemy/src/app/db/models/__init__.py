"""All SQLAlchemy models, centralized (litestar-fullstack convention).

Domains import models from here — never from each other.
"""

from app.db.models._book import Book

__all__ = ("Book",)
