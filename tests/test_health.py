from starlette.testclient import TestClient
from enterprise_mcp.app import app

def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.text == "OK"