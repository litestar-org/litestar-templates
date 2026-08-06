# Litestar Advanced Alchemy Starter (domain-driven)

Database-backed CRUD with
[Advanced Alchemy](https://docs.advanced-alchemy.litestar.dev/), structured
the way [litestar-fullstack](https://github.com/litestar-org/litestar-fullstack)
structures its Python side: centralized models, self-contained domain
packages, and one application core plugin.

## Layout

```
src/app/
├── config.py               DATABASE_URL + SQLAlchemy config factory
├── db/
│   └── models/             ALL SQLAlchemy models, centralized
│       └── _book.py        (private modules, re-exported in __init__)
├── domain/
│   └── books/              one package per bounded context
│       ├── controllers.py  HTTP layer — thin: validate, delegate, return
│       ├── deps.py         request-scoped service provider
│       ├── schemas.py      msgspec wire-format models
│       └── services.py     SQLAlchemyAsyncRepositoryService — owns data access
└── server/
    ├── core.py             ApplicationCore (InitPluginProtocol) — wires all domains
    └── asgi.py             create_app() factory + SQLAlchemyPlugin
tests/
└── integration/            full request/response round-trips on a temp database
```

## Run

```sh
uv sync
uv run litestar --app-dir src run --reload
# or, fullstack-style:
LITESTAR_APP=app.server.asgi:app uv run litestar run --reload
```

- API: <http://127.0.0.1:8000/books>
- OpenAPI docs: <http://127.0.0.1:8000/schema>

Uses SQLite (`db.sqlite3`) by default so it runs with zero setup. Point
`DATABASE_URL` at PostgreSQL when ready (add `asyncpg` to the dependencies
first):

```sh
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db uv run litestar --app-dir src run
```

## Test

```sh
uv run pytest
```

## What it shows

- **Centralized models** (`db/models/`) — domains import models from one
  place, never from each other
- **Domain isolation** — `books` owns its controllers, schemas, services, and
  providers; `server/core.py` is the only module that knows every domain
- `SQLAlchemyAsyncRepositoryService` + typed repository — data access lives in
  the service layer, handlers stay thin
- `SQLAlchemyPlugin` session management with per-request autocommit
  (`before_send_handler="autocommit"`)
- Advanced Alchemy's first-party `exception_to_http_response` — repository
  errors map to 404/409 automatically
- An app factory (`create_app`) so tests run against an isolated database

## Growing it

- New bounded context → model in `db/models/`, package under `domain/`,
  registered in `server/core.py`.
- Migrations: Advanced Alchemy bundles Alembic —
  `uv run litestar --app-dir src database make-migrations` / `database upgrade`
  replace `create_all=True` for real deployments.
- Pagination and filtering: `advanced_alchemy.filters` +
  `create_filter_dependencies`.
