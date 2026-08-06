# Litestar Middleware Starter

A custom ASGI middleware for [Litestar](https://litestar.dev) built on the
`ASGIMiddleware` base class. The example measures request duration and adds
an `X-Response-Time` header to every HTTP response.

## Run

```sh
uv sync
uv run litestar run --reload
curl -i http://127.0.0.1:8000/
```

## Test

```sh
uv run pytest
```

## What it shows

- Subclassing `litestar.middleware.ASGIMiddleware`
- Scope filtering with `scopes = (ScopeType.HTTP,)` (WebSockets untouched)
- Request exclusions with `should_bypass_for_scope` (the Litestar-3-ready
  alternative to `exclude_path_pattern`)
- Mutating outgoing headers via `MutableScopeHeaders` in a send wrapper

## Next steps

- Prefer Litestar's built-in configs (`CORSConfig`, `CSRFConfig`,
  `CompressionConfig`, `AllowedHostsConfig`) before writing custom middleware.
- Middleware docs: <https://docs.litestar.dev/latest/usage/middleware/>
