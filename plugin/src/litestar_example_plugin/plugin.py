"""An example Litestar plugin: adds a configurable health-check endpoint.

Implements ``InitPlugin`` — the hook that lets a plugin mutate the
``AppConfig`` (routes, dependencies, middleware, state, lifespan) before the
app finishes booting.
"""

from dataclasses import dataclass

from litestar import get
from litestar.config.app import AppConfig
from litestar.plugins import InitPluginProtocol


@dataclass
class HealthCheckConfig:
    """Configuration for :class:`HealthCheckPlugin`."""

    path: str = "/health"
    """Route path of the health-check endpoint."""

    include_in_schema: bool = False
    """Whether the endpoint shows up in the OpenAPI schema."""


class HealthCheckPlugin(InitPluginProtocol):
    """Register a health-check route on the application."""

    __slots__ = ("config",)

    def __init__(self, config: HealthCheckConfig | None = None) -> None:
        self.config = config or HealthCheckConfig()

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        @get(
            self.config.path,
            include_in_schema=self.config.include_in_schema,
            name="health_check",
        )
        async def health_check() -> dict[str, str]:
            return {"status": "ok"}

        app_config.route_handlers.append(health_check)
        return app_config
