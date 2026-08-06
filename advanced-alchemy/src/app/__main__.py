"""CLI entry point (litestar-fullstack pattern).

Exposed as the ``app`` script in pyproject.toml, so every Litestar CLI
command works without ``--app-dir`` or ``LITESTAR_APP``:

    uv run app run --reload
    uv run app routes
    uv run app database make-migrations
"""

import os
import sys


def run_cli() -> None:
    """Point the Litestar CLI at the app factory and hand over."""
    os.environ.setdefault("LITESTAR_APP", "app.server.asgi:create_app")

    try:
        from litestar.cli.main import litestar_group
    except ImportError as exc:
        print("Could not load the Litestar CLI:", exc, file=sys.stderr)
        sys.exit(1)

    litestar_group()


if __name__ == "__main__":
    run_cli()
