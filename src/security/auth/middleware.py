from __future__ import annotations
from httpx import request
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse

from enterprise_mcp.security.auth.strategy import AuthStrategy, AuthError
from enterprise_mcp.security.models import Principal

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Attaches request.state.principal after authenticating using the provided AuthStrategy.
    Protects configured paths (eg. /mcp). Leaves public paths (eg. /health) open.
    """
    def __init__(
            self,
            app,
            strategy: AuthStrategy,
            protected_prefixes: tuple[str, ...] = ("/mcp",),
            public_prefixes: tuple[str, ...] = ("/health",),
    ):
        super().__init__(app)
        self._strategy = strategy
        self._protected_prefixes = protected_prefixes
        self._public_prefixes = public_prefixes

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path

        is_protected = any(path.startswith(prefix) for prefix in self._protected_prefixes)
        is_public = any(path.startswith(prefix) for prefix in self._public_prefixes)

        if is_public:
            request.state.principal = Principal(subject="anonymous", display_name="Anonymous User")
            return await call_next(request)

        if is_protected:
            try:
                principal = await self._strategy.authenticate(request)
                request.state.principal = principal
            except AuthError as e:
                return JSONResponse(
                    status_code=401,
                    content={"detail": str(e)},
                )

        return await call_next(request)
    
