# Litestar Plugin Starter

A starter for **authoring a Litestar plugin** as an installable package. The
example plugin adds a configurable health-check endpoint via the
`InitPluginProtocol` hook.

## Layout

```
src/litestar_example_plugin/   the plugin package (rename to yours)
example_app.py                 an app consuming the plugin
tests/                         plugin behavior tests
```

## Run the example app

```sh
uv sync
uv run litestar --app example_app:app run --reload
curl http://127.0.0.1:8000/health
```

## Test

```sh
uv run pytest
```

## What it shows

- `InitPluginProtocol.on_app_init` — mutating `AppConfig` (routes, deps,
  middleware, state, lifespan) before the app boots
- A dataclass config object, the convention used by first-party plugins
- src-layout packaging with hatchling, ready for PyPI
- Testing a plugin by building a fresh `Litestar` app per test

## Next steps

- Other plugin protocols: `CLIPluginProtocol` (add CLI commands),
  `SerializationPluginProtocol`, `OpenAPISchemaPluginProtocol`.
- Plugin docs: <https://docs.litestar.dev/latest/usage/plugins/>
