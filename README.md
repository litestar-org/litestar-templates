# Litestar Templates

[![CI](https://github.com/litestar-org/litestar-templates/actions/workflows/ci.yml/badge.svg)](https://github.com/litestar-org/litestar-templates/actions/workflows/ci.yml)

Official starter templates for the [Litestar](https://litestar.dev) web framework.
One folder per starter — every starter is a small, self-contained, tested
[uv](https://docs.astral.sh/uv/) project that boots out of the box.

## Starters

| Name | Description |
| --- | --- |
| [`minimal`](./minimal) | Smallest possible Litestar app — a single route, ready to run. |
| [`api`](./api) | Domain-driven REST API — bounded contexts (controllers/schemas/services) composed by an application core plugin, litestar-fullstack style. |
| [`middleware`](./middleware) | Custom ASGI middleware — response timing header with scope filtering. |
| [`plugin`](./plugin) | Plugin-authoring starter — a packaged `InitPlugin` with config and tests. |
| [`jwt-auth`](./jwt-auth) | JWT authentication — login endpoint, protected routes, auth tests. |
| [`advanced-alchemy`](./advanced-alchemy) | Database CRUD with Advanced Alchemy's repository/service layer. |

The machine-readable list lives in [`templates.json`](./templates.json).

Starters track the **latest stable Litestar** and deliberately use only
Litestar-3-ready APIs (`FromPath`/`NamedDependency` markers,
`should_bypass_for_scope`, no deprecated inference) — test suites are kept
free of `LitestarDeprecationWarning` so the jump to Litestar 3 is a version
bump, not a rewrite.

## Usage

Grab a single starter without cloning the whole repository:

```sh
# with giget (Node)
npx giget gh:litestar-org/litestar-templates/minimal my-app

# with git sparse checkout
git clone --depth 1 --filter=blob:none --sparse https://github.com/litestar-org/litestar-templates
cd litestar-templates && git sparse-checkout set minimal
```

Then run it:

```sh
cd my-app
uv sync
uv run litestar run --reload
```

Every starter serves its API at `http://127.0.0.1:8000` and interactive
OpenAPI docs at `http://127.0.0.1:8000/schema`.

## Development

Each starter is an independent uv project:

```sh
cd <starter>
uv sync            # install dependencies (incl. dev group)
uv run pytest      # run the starter's tests
uv run litestar run --reload
```

CI runs every starter's test suite on each push (see
[`.github/workflows/ci.yml`](./.github/workflows/ci.yml)).

## Contributing

- Keep starters small and focused — one concept per starter.
- Every starter must boot with `uv run litestar run` and pass `uv run pytest`.
- Adding a starter: create the folder, add it to `templates.json`, the table
  above, and the CI matrix.

## License

[MIT](./LICENSE)
