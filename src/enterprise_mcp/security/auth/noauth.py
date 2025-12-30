from enterprise_mcp.security.auth.strategy import AuthStrategy


class NoAuthStrategy(AuthStrategy):
    """No authentication strategy - allows all requests"""
    
    def authenticate(self, token: str | None) -> dict | None:
        return {"user": "anonymous"}
