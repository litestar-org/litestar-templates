from litestar import Request, Response
from litestar.status_codes import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class ApplicationError(Exception):
    """Base class for all domain errors."""


class NotFoundError(ApplicationError):
    """The requested entity does not exist."""


def exception_to_http_response(
    request: Request, exc: ApplicationError
) -> Response[dict[str, str]]:
    status_code = (
        HTTP_404_NOT_FOUND
        if isinstance(exc, NotFoundError)
        else HTTP_500_INTERNAL_SERVER_ERROR
    )
    return Response(
        status_code=status_code,
        content={"detail": str(exc) or exc.__class__.__name__},
    )
