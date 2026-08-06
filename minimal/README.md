# Litestar Minimal Starter

The smallest possible [Litestar](https://litestar.dev) application: a single
async route handler and nothing else.

## Run

```sh
uv sync
uv run litestar run --reload
```

- App: <http://127.0.0.1:8000/>
- OpenAPI docs: <http://127.0.0.1:8000/schema>

## Test

```sh
uv run pytest
```

## Next steps

- Add routes and group them in a `Controller` — see the [`api`](../api) starter.
- Litestar documentation: <https://docs.litestar.dev/>
