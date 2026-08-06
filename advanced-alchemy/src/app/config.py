import os

from advanced_alchemy.extensions.litestar import SQLAlchemyAsyncConfig

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3")


def get_db_config(database_url: str = DATABASE_URL) -> SQLAlchemyAsyncConfig:
    return SQLAlchemyAsyncConfig(
        connection_string=database_url,
        # For real deployments, replace create_all with Alembic migrations
        # (`litestar database make-migrations` / `database upgrade`).
        create_all=True,
        # Commit on 2xx responses, roll back otherwise (and on exceptions).
        before_send_handler="autocommit",
    )
