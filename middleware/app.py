"""Custom ASGI middleware: adds an `X-Response-Time` header to every response.

Shows the `ASGIMiddleware` base class, scope filtering (HTTP only), request
exclusions via `should_bypass_for_scope`, and how to mutate outgoing response
headers.
"""

import time

from litestar import Litestar, get
from litestar.datastructures import MutableScopeHeaders
from litestar.enums import ScopeType
from litestar.middleware import ASGIMiddleware
from litestar.types import ASGIApp, Message, Receive, Scope, Send


class TimingMiddleware(ASGIMiddleware):
    """Measure request duration and expose it as a response header."""

    scopes = (ScopeType.HTTP,)

    @staticmethod
    def should_bypass_for_scope(scope: Scope) -> bool:
        return scope["path"].startswith("/schema")

    async def handle(
        self, scope: Scope, receive: Receive, send: Send, next_app: ASGIApp
    ) -> None:
        start = time.perf_counter()

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                duration_ms = (time.perf_counter() - start) * 1000
                headers = MutableScopeHeaders(message)
                headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
            await send(message)

        await next_app(scope, receive, send_wrapper)


@get("/")
async def index() -> dict[str, str]:
    return {"message": "Check the X-Response-Time response header!"}


app = Litestar(route_handlers=[index], middleware=[TimingMiddleware()])
