from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from enterprise_mcp.security.auth.strategy import AuthStrategy


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for authentication"""
    
    def __init__(self, app, strategy: AuthStrategy, protected_prefixes: list[str] | None = None, public_prefixes: list[str] | None = None):
        super().__init__(app)
        self.strategy = strategy
        self.protected_prefixes = protected_prefixes or []
        self.public_prefixes = public_prefixes or []
    
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Check if path is public
        if any(path.startswith(prefix) for prefix in self.public_prefixes):
            return await call_next(request)
        
        # Check if path is protected
        if any(path.startswith(prefix) for prefix in self.protected_prefixes):
            # Get token from Authorization header
            auth_header = request.headers.get("Authorization", "")
            token = None
            
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
            
            # Authenticate
            user = self.strategy.authenticate(token)
            if not user:
                return JSONResponse({"error": "Unauthorized"}, status_code=401)
            
            # Store user info in request state
            request.state.user = user
        
        return await call_next(request)
