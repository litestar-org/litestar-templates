from litestar.datastructures import State

from app.domain.todos.services import TodoService

TODOS_SERVICE_STATE_KEY = "todos_service"


async def provide_todos_service(state: State) -> TodoService:
    """Return the app-scoped service instance placed in state by the core plugin."""
    return state[TODOS_SERVICE_STATE_KEY]
