"""A small REST API: CRUD for todo items, backed by an in-memory store.

Swap the `TodoStore` for a real database when you outgrow it — the
`advanced-alchemy` starter shows the recommended way.
"""

from uuid import UUID, uuid4

import msgspec
from litestar import Controller, Litestar, delete, get, post, put
from litestar.exceptions import NotFoundException
from litestar.openapi import OpenAPIConfig
from litestar.params import FromPath


class TodoCreate(msgspec.Struct):
    """Payload for creating or updating a todo item."""

    title: str
    done: bool = False


class Todo(msgspec.Struct):
    """A todo item."""

    id: UUID
    title: str
    done: bool


class TodoStore:
    """In-memory storage. Replace with a database-backed service in real apps."""

    def __init__(self) -> None:
        self._items: dict[UUID, Todo] = {}

    def list(self) -> list[Todo]:
        return list(self._items.values())

    def get(self, todo_id: UUID) -> Todo:
        try:
            return self._items[todo_id]
        except KeyError as exc:
            raise NotFoundException(detail=f"Todo {todo_id} not found") from exc

    def add(self, data: TodoCreate) -> Todo:
        todo = Todo(id=uuid4(), title=data.title, done=data.done)
        self._items[todo.id] = todo
        return todo

    def replace(self, todo_id: UUID, data: TodoCreate) -> Todo:
        self.get(todo_id)
        todo = Todo(id=todo_id, title=data.title, done=data.done)
        self._items[todo_id] = todo
        return todo

    def remove(self, todo_id: UUID) -> None:
        self.get(todo_id)
        del self._items[todo_id]


store = TodoStore()


class TodoController(Controller):
    """CRUD endpoints for todo items."""

    path = "/todos"
    tags = ["todos"]

    @get("/")
    async def list_todos(self) -> list[Todo]:
        return store.list()

    @get("/{todo_id:uuid}")
    async def get_todo(self, todo_id: FromPath[UUID]) -> Todo:
        return store.get(todo_id)

    @post("/")
    async def create_todo(self, data: TodoCreate) -> Todo:
        return store.add(data)

    @put("/{todo_id:uuid}")
    async def update_todo(self, todo_id: FromPath[UUID], data: TodoCreate) -> Todo:
        return store.replace(todo_id, data)

    @delete("/{todo_id:uuid}")
    async def delete_todo(self, todo_id: FromPath[UUID]) -> None:
        store.remove(todo_id)


app = Litestar(
    route_handlers=[TodoController],
    openapi_config=OpenAPIConfig(title="Todo API", version="0.1.0"),
)
