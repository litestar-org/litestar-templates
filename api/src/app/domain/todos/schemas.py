"""Wire-format schemas for the todos domain (msgspec Structs)."""

from uuid import UUID

import msgspec


class TodoCreate(msgspec.Struct):
    """Payload for creating or replacing a todo item."""

    title: str
    done: bool = False


class Todo(msgspec.Struct):
    """A todo item as returned by the API."""

    id: UUID
    title: str
    done: bool
