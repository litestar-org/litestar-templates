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
