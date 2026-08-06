"""Application core: composes routes and error handling.

Same pattern as litestar-fullstack's ``ApplicationCore`` — one
``InitPluginProtocol`` plugin that wires every domain into the app. Database
plumbing stays in ``SQLAlchemyPlugin`` (see ``asgi.py``); repository errors
map to HTTP responses via Advanced Alchemy's first-party handler.
"""

from advanced_alchemy.exceptions import RepositoryError
from advanced_alchemy.extensions.litestar.exception_handler import (
    exception_to_http_response,
)
from litestar.config.app import AppConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.plugins import InitPluginProtocol

from app.domain.books.controllers import BookController


class ApplicationCore(InitPluginProtocol):
    """Configure the Litestar application with routes and handlers."""

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.openapi_config = OpenAPIConfig(
            title="Book API",
            version="0.1.0",
            path="/schema",
        )
        app_config.route_handlers.append(BookController)
        # NotFoundError -> 404, Duplicate/Integrity -> 409, etc.
        app_config.exception_handlers[RepositoryError] = exception_to_http_response
        return app_config
