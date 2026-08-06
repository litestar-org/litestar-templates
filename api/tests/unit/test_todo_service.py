import pytest

from app.domain.todos.schemas import TodoCreate
from app.domain.todos.services import TodoService
from app.lib.exceptions import NotFoundError

pytestmark = pytest.mark.anyio


async def test_create_and_get() -> None:
    service = TodoService()
    todo = await service.create(TodoCreate(title="learn DDD"))
    assert (await service.get(todo.id)).title == "learn DDD"


async def test_get_missing_raises_domain_error() -> None:
    service = TodoService()
    todo = await service.create(TodoCreate(title="x"))
    await service.delete(todo.id)
    with pytest.raises(NotFoundError):
        await service.get(todo.id)


async def test_replace_keeps_id() -> None:
    service = TodoService()
    todo = await service.create(TodoCreate(title="before"))
    replaced = await service.replace(todo.id, TodoCreate(title="after", done=True))
    assert replaced.id == todo.id
    assert replaced.done is True
