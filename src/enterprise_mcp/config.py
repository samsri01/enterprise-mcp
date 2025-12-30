from pydantic import BaseModel, ConfigDict
import os


class Settings(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        validate_default=True,
    )

    app_name: str = "EnterpriseMCP"
    debug: bool = True

    # auth: "none" or "jwt"
    auth_mode: str = os.getenv("AUTH_MODE", "none").lower()

    # for jwt mode (HS256 bootstrap)
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
    jwt_issuer: str | None = os.getenv("JWT_ISSUER")
    jwt_audience: str | None = os.getenv("JWT_AUDIENCE")


settings = Settings()
