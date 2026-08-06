"""Business logic for the todos domain.

Services own data access and raise domain errors — they know nothing about
HTTP. This one stores todos in memory; swap the internals for a real
repository (see the ``advanced-alchemy`` starter) without touching the
controllers.
"""

from uuid import UUID, uuid4

from app.domain.todos.schemas import Todo, TodoCreate
from app.lib.exceptions import NotFoundError


class TodoService:
    """In-memory CRUD for todo items."""

    def __init__(self) -> None:
        self._items: dict[UUID, Todo] = {}

    async def list(self) -> list[Todo]:
        return list(self._items.values())

    async def get(self, todo_id: UUID) -> Todo:
        try:
            return self._items[todo_id]
        except KeyError as exc:
            raise NotFoundError(f"Todo {todo_id} not found") from exc

    async def create(self, data: TodoCreate) -> Todo:
        todo = Todo(id=uuid4(), title=data.title, done=data.done)
        self._items[todo.id] = todo
        return todo

    async def replace(self, todo_id: UUID, data: TodoCreate) -> Todo:
        await self.get(todo_id)
        todo = Todo(id=todo_id, title=data.title, done=data.done)
        self._items[todo_id] = todo
        return todo

    async def delete(self, todo_id: UUID) -> None:
        await self.get(todo_id)
        del self._items[todo_id]
