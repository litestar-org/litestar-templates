import msgspec


class BookCreate(msgspec.Struct):
    """Payload for creating a book."""

    title: str
    author: str
