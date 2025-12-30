import os
import jwt
import pytest
from starlette.testclient import TestClient


def _make_test_jwt(secret: str) -> str:
    # Minimal claims; JwtAuthStrategy reads "sub" and optional roles/name
    payload = {
        "sub": "user-123",
        "name": "Test User",
        "roles": ["seller"],
    }
    return jwt.encode(payload, secret, algorithm="HS256")


@pytest.fixture
def app_jwt_mode(monkeypatch):
    """
    Build a fresh app with AUTH_MODE=jwt.
    We import enterprise_mcp.app AFTER setting env vars so settings are loaded correctly.
    """
    monkeypatch.setenv("AUTH_MODE", "jwt")
    monkeypatch.setenv("JWT_SECRET", "test-secret")

    # Important: reload modules so Settings() re-reads env vars.
    import importlib
    import enterprise_mcp.config as config
    import enterprise_mcp.app as appmod

    importlib.reload(config)
    importlib.reload(appmod)

    return appmod.app


def test_mcp_requires_auth_in_jwt_mode(app_jwt_mode):
    client = TestClient(app_jwt_mode)
    r = client.post("/mcp/")  # no Authorization header
    assert r.status_code == 401
    body = r.json()
    assert body["error"].lower() == "unauthorized"


def test_mcp_allows_request_with_valid_bearer_token(app_jwt_mode):
    client = TestClient(app_jwt_mode)

    token = _make_test_jwt("test-secret")
    r = client.post("/mcp/", headers={"Authorization": f"Bearer {token}"})

    # The exact status after auth depends on MCP payload/body.
    # We only assert that auth didn't block it.
    assert r.status_code != 401
