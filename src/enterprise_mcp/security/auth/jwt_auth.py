import jwt
from enterprise_mcp.security.auth.strategy import AuthStrategy


class JwtAuthStrategy(AuthStrategy):
    """JWT-based authentication strategy"""
    
    def __init__(self, secret: str, issuer: str | None = None, audience: str | None = None):
        self.secret = secret
        self.issuer = issuer
        self.audience = audience
    
    def authenticate(self, token: str | None) -> dict | None:
        if not token:
            return None
        
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=["HS256"],
                issuer=self.issuer,
                audience=self.audience,
            )
            return payload
        except jwt.InvalidTokenError:
            return None
