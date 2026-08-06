# Litestar JWT Auth Starter

JWT authentication with Litestar's first-party
[`litestar.security.jwt`](https://docs.litestar.dev/latest/usage/security/jwt.html):
a login endpoint that issues tokens and routes protected app-wide by default.

## Run

```sh
uv sync
uv run litestar run --reload

# get a token (returned in the Authorization response header)
curl -i -X POST http://127.0.0.1:8000/login \
  -H 'Content-Type: application/json' \
  -d '{"username": "admin", "password": "s3cret"}'

# call a protected route
curl http://127.0.0.1:8000/me -H 'Authorization: Bearer <token>'
```

## Test

```sh
uv run pytest
```

## What it shows

- `JWTAuth[User]` wired via `on_app_init`: protection is the default,
  `exclude` lists the public routes
- `retrieve_user_handler` mapping a decoded `Token` to your user object
- `request.user` typed access in handlers
- Auth flow tests: login, wrong password, missing token, valid token

## Before production

- Replace the in-memory user dict with a real database.
- Hash passwords (`argon2-cffi`, `passlib`); never store plaintext.
- Set `JWT_SECRET` from the environment; rotate it like any credential.
- Consider `JWTCookieAuth` for browser clients (httpOnly cookies).
