# Litestar API Starter

A REST API built with [Litestar](https://litestar.dev): a `Controller` with
full CRUD routes, [msgspec](https://jcristharif.com/msgspec/) models with
request validation, and generated OpenAPI documentation.

## Run

```sh
uv sync
uv run litestar run --reload
```

- API: <http://127.0.0.1:8000/todos>
- OpenAPI docs: <http://127.0.0.1:8000/schema>

## Test

```sh
uv run pytest
```

## What it shows

- Grouping routes in a `Controller` with path parameters (`{todo_id:uuid}`)
- msgspec `Struct` models for request/response payloads with validation
- Idiomatic error handling with `NotFoundException`
- OpenAPI configuration and schema tests

## Next steps

- Persist data with a real database — see the
  [`advanced-alchemy`](../advanced-alchemy) starter.
- Protect routes with authentication — see the [`jwt-auth`](../jwt-auth)
  starter.
