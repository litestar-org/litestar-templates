from litestar import Litestar, get

from litestar_example_plugin import HealthCheckConfig, HealthCheckPlugin


@get("/")
async def index() -> dict[str, str]:
    return {"message": "See /health, added by HealthCheckPlugin"}


app = Litestar(
    route_handlers=[index],
    plugins=[HealthCheckPlugin(HealthCheckConfig(path="/health"))],
)
