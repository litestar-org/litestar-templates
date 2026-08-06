# Litestar API Starter (domain-driven)

A REST API structured the way
[litestar-fullstack](https://github.com/litestar-org/litestar-fullstack)
structures its Python side: self-contained **domain packages** composed by a
single **application core plugin**. Storage is in-memory so the pattern stays
front and center — swap the service internals for a database when ready.

## Layout

```
src/app/
├── domain/                 one package per bounded context
│   ├── system/
│   │   └── controllers.py  health endpoint
│   └── todos/
│       ├── controllers.py  HTTP layer — thin: validate, delegate, return
│       ├── deps.py         dependency providers for this domain
│       ├── schemas.py      msgspec wire-format models
│       └── services.py     business logic — owns data, raises domain errors
├── lib/
│   └── exceptions.py       domain errors + the single error→HTTP mapping
└── server/
    ├── core.py             ApplicationCore (InitPluginProtocol) — wires all domains
    └── asgi.py             create_app() factory + ASGI entry point
tests/
├── unit/                   service tests, no HTTP
└── integration/            full request/response round-trips
```

## Run

```sh
uv sync
uv run litestar --app-dir src run --reload
# or, fullstack-style:
LITESTAR_APP=app.server.asgi:app uv run litestar run --reload
```

- API: <http://127.0.0.1:8000/todos>
- OpenAPI docs: <http://127.0.0.1:8000/schema>

## Test

```sh
uv run pytest
```

## What it shows

- **Domain isolation** — `todos` owns its controllers, schemas, services, and
  providers; `server/core.py` is the only module that knows every domain.
- **Services own logic** — handlers never touch storage or raise HTTP errors;
  services raise `NotFoundError` and one registered handler maps it to a 404.
- **App factory** — `create_app()` builds isolated instances, so tests never
  share state.
- **3.0-ready handler style** — `FromPath[UUID]` and `NamedDependency[...]`
  markers throughout.

## Growing it

- New bounded context → new package under `domain/`, registered in
  `server/core.py`.
- Real persistence → replace `TodoService` internals with an Advanced Alchemy
  repository/service (see the [`advanced-alchemy`](../advanced-alchemy)
  starter); controllers don't change.
- Auth → add guards per domain (see the [`jwt-auth`](../jwt-auth) starter).
