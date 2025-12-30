from __future__ import annotations
from typing import Protocol
from starlette.requests import Request
from enterprise_mcp.security.models import Principal

class AuthError(Exception):
    """Custom exception for authentication errors."""
    pass

class AuthStrategy(Protocol):
    async def authenticate(self, request: Request) -> Principal:
        """Authenticate the incoming request and return a Principal.

        Args:
            request (Request): The incoming HTTP request."""