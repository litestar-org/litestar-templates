import os

import msgspec
from litestar import Litestar, Request, Response, get, post
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.security.jwt import JWTAuth, Token


class User(msgspec.Struct):
    """An application user."""

    id: str
    name: str


class Credentials(msgspec.Struct):
    """Login payload."""

    username: str
    password: str


# Demo store; replace with a real database and hashed passwords.
USERS: dict[str, User] = {"admin": User(id="admin", name="Admin User")}
PASSWORDS: dict[str, str] = {"admin": "s3cret"}

# HMAC-SHA256 keys must be at least 32 bytes (RFC 7518 §3.2).
TOKEN_SECRET = os.environ.get("JWT_SECRET", "insecure-dev-only-secret-change-me-now")


async def retrieve_user_handler(
    token: Token, connection: ASGIConnection
) -> User | None:
    """Map a decoded token back to a user. Returning None rejects the request."""
    return USERS.get(token.sub)


jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=TOKEN_SECRET,
    exclude=["/login", "/schema"],
)


@post("/login")
async def login(data: Credentials) -> Response[User]:
    if PASSWORDS.get(data.username) != data.password:
        raise NotAuthorizedException(detail="Invalid credentials")
    user = USERS[data.username]
    return jwt_auth.login(identifier=user.id, response_body=user)


@get("/me")
async def me(request: Request[User, Token, None]) -> User:
    return request.user


app = Litestar(route_handlers=[login, me], on_app_init=[jwt_auth.on_app_init])
