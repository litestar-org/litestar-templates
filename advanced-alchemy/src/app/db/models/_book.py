from advanced_alchemy.extensions.litestar import base
from sqlalchemy.orm import Mapped


class Book(base.UUIDAuditBase):
    """A book. UUID primary key and audit timestamps come from the base."""

    __tablename__ = "book"

    title: Mapped[str]
    author: Mapped[str]
