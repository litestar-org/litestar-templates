"""ASGI entry point. Run with `uv run litestar --app-dir src run` (see README)."""

from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar import Litestar

from app.config import DATABASE_URL, get_db_config
from app.server.core import ApplicationCore


def create_app(database_url: str = DATABASE_URL) -> Litestar:
    """App factory — tests inject their own database URL."""
    return Litestar(
        plugins=[
            ApplicationCore(),
            SQLAlchemyPlugin(config=get_db_config(database_url)),
        ],
    )


app = create_app()
