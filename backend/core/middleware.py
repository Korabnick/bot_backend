from fastapi import Request, status
from fastapi.responses import JSONResponse

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from backend.core.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        auth_key = request.headers.get('Authorization')
        if isinstance(auth_key, str) and auth_key != f"Bearer {settings.AUTH_KEY}" and str(request.url).split('/')[-1] not in ['openapi.json ', 'swagger', 'metrics']:
            return JSONResponse(content={'err': "No auth header"}, status_code=status.HTTP_401_UNAUTHORIZED)
        response = await call_next(request)
        return response
