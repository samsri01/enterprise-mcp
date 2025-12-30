from abc import ABC, abstractmethod


class AuthStrategy(ABC):
    """Base class for authentication strategies"""
    
    @abstractmethod
    def authenticate(self, token: str | None) -> dict | None:
        """
        Authenticate using the provided token.
        Returns user info dict if valid, None otherwise.
        """
        pass
