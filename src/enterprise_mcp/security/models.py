from pydantic import BaseModel


class User(BaseModel):
    """User model"""
    username: str
    email: str | None = None
