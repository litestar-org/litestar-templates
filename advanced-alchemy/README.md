# Litestar Advanced Alchemy Starter

Database-backed CRUD with
[Advanced Alchemy](https://docs.advanced-alchemy.litestar.dev/) — the
Litestar-native service/repository layer on top of SQLAlchemy 2.0.

## Run

```sh
uv sync
uv run litestar run --reload
```

- API: <http://127.0.0.1:8000/books>
- OpenAPI docs: <http://127.0.0.1:8000/schema>

Uses SQLite (`db.sqlite3`) by default so it runs with zero setup. Point
`DATABASE_URL` at PostgreSQL when ready:

```sh
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db uv run litestar run
```

(add `asyncpg` to the dependencies first)

## Test

```sh
uv run pytest
```

## What it shows

- `UUIDAuditBase` models (UUID PK + `created_at`/`updated_at` for free)
- `SQLAlchemyAsyncRepositoryService` — data access lives in a service, not in
  route handlers
- `SQLAlchemyPlugin` session management with per-request autocommit
- `SQLAlchemyDTO` for automatic model serialization
- An app factory (`create_app`) so tests run against an isolated database

## Next steps

- Migrations: Advanced Alchemy bundles Alembic —
  `uv run litestar database make-migrations` / `database upgrade` replace
  `create_all=True` for real deployments.
- Pagination and filtering: `advanced_alchemy.filters` +
  `create_filter_dependencies`.
