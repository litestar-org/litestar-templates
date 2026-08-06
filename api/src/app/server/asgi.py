from litestar import Litestar

from app.server.core import ApplicationCore


def create_app() -> Litestar:
    """App factory — tests build isolated instances from this."""
    return Litestar(plugins=[ApplicationCore()])


app = create_app()
