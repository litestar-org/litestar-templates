from uuid import UUID

from litestar import Controller, delete, get, post, put
from litestar.di import NamedDependency, Provide
from litestar.params import FromPath

from app.domain.todos.deps import provide_todos_service
from app.domain.todos.schemas import Todo, TodoCreate
from app.domain.todos.services import TodoService


class TodoController(Controller):
    path = "/todos"
    tags = ["todos"]
    dependencies = {"todos_service": Provide(provide_todos_service)}

    @get("/")
    async def list_todos(
        self, todos_service: NamedDependency[TodoService]
    ) -> list[Todo]:
        return await todos_service.list()

    @get("/{todo_id:uuid}")
    async def get_todo(
        self, todos_service: NamedDependency[TodoService], todo_id: FromPath[UUID]
    ) -> Todo:
        return await todos_service.get(todo_id)

    @post("/")
    async def create_todo(
        self, todos_service: NamedDependency[TodoService], data: TodoCreate
    ) -> Todo:
        return await todos_service.create(data)

    @put("/{todo_id:uuid}")
    async def update_todo(
        self,
        todos_service: NamedDependency[TodoService],
        todo_id: FromPath[UUID],
        data: TodoCreate,
    ) -> Todo:
        return await todos_service.replace(todo_id, data)

    @delete("/{todo_id:uuid}")
    async def delete_todo(
        self, todos_service: NamedDependency[TodoService], todo_id: FromPath[UUID]
    ) -> None:
        await todos_service.delete(todo_id)
