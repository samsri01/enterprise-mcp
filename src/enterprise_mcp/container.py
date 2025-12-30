from __future__ import annotations

from enterprise_mcp.config import settings
from enterprise_mcp.security.auth.noauth import NoAuthStrategy
from enterprise_mcp.security.auth.jwt_auth import JwtAuthStrategy
from enterprise_mcp.security.auth.strategy import AuthStrategy


def build_auth_strategy() -> AuthStrategy:
    if settings.auth_mode == "jwt":
        return JwtAuthStrategy(
            secret=settings.jwt_secret,
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
        )
    return NoAuthStrategy()
