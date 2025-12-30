from __future__ import annotations
from starlette.requests import Request
from enterprise_mcp.security.models import Principal
from enterprise_mcp.security.auth.strategy import AuthStrategy

class NoAuthStrategy(AuthStrategy):
    async def authenticate(self, request: Request) -> Principal:
        return Principal(subject="anonymous", display_name="Anonymous User")