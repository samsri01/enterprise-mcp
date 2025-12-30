from __future__ import annotations

import jwt
from starlette.requests import Request
from enterprise_mcp.security.models import Principal
from enterprise_mcp.security.auth.strategy import AuthStrategy, AuthError

class JWTAuthStrategy(AuthStrategy):
    """ JWT auth (HS256) for local/prod bootstrap.
    
    Later upgrade: OIDC/JWKS validation (RS256) + issuer/audience checks.
    
    """

    def __init__(
            self,
            secret: str,
            issuer: str | None = None,
            audience: str | None = None,
    ) -> None:
        self._secret = secret
        self._issuer = issuer
        self._audience = audience
    
    async def authenticate(self, request: Request) -> Principal:
        auth_header = request.headers.get("Authorization") or request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthError("Missing or invalid Authorization header")
        
        token = auth_header[len("Bearer "):]
        
        try:
            decoded = jwt.decode(
                token,
                self._secret,
                algorithms=["HS256"],
                issuer=self._issuer,
                audience=self._audience,
            )
        except jwt.PyJWTError as e:
            raise AuthError(f"JWT validation error: {str(e)}") from e
        
        subject = decoded.get("sub")
        if not subject:
            raise AuthError("JWT missing 'sub' claim")
        
        display_name = decoded.get("name")
        roles = tuple(decoded.get("roles", []))
        claims = {k: v for k, v in decoded.items() if k not in {"sub", "name", "roles"}}
        
        return Principal(
            subject=subject,
            display_name=display_name,
            roles=roles,
            claims=claims,
        )