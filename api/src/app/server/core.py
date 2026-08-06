from litestar.config.app import AppConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.plugins import InitPluginProtocol

from app.domain.system.controllers import SystemController
from app.domain.todos.controllers import TodoController
from app.domain.todos.deps import TODOS_SERVICE_STATE_KEY
from app.domain.todos.services import TodoService
from app.lib.exceptions import ApplicationError, exception_to_http_response


class ApplicationCore(InitPluginProtocol):
    """Configure the Litestar application with routes, state, and handlers."""

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.openapi_config = OpenAPIConfig(
            title="Todo API",
            version="0.1.0",
            path="/schema",
        )
        app_config.route_handlers.extend([SystemController, TodoController])
        # App-scoped service instance; domains fetch it via their deps module.
        app_config.state[TODOS_SERVICE_STATE_KEY] = TodoService()
        app_config.exception_handlers[ApplicationError] = exception_to_http_response
        return app_config
