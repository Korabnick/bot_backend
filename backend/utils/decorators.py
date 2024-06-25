from functools import wraps
from typing import Callable, Union

from starlette import status
from fastapi.responses import JSONResponse

from backend.utils.exceptions import NotFoundException, IncorrectDataException


def create_error_response(error: Union[Exception, str], status_code: int = status.HTTP_400_BAD_REQUEST) -> JSONResponse:
    return JSONResponse({"error": str(error)}, status_code=status_code)


def handle_domain_exceptions(func: Callable) -> Callable:
    """Декоратор для обработки DomainException."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NotFoundException as e:
            return create_error_response(e, status_code=status.HTTP_404_NOT_FOUND)
        except IncorrectDataException as e:
            return create_error_response(e)
    return wrapper
