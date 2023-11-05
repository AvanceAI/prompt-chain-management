# tests/test_security.py
import os
from fastapi.testclient import TestClient

def test_cors_headers(mocker):
    """
    Test to ensure that CORS headers are set correctly.
    """
    from src.main import app
    client = TestClient(app)

    mocker.patch.dict(os.environ, {"CORS_ORIGINS": "http://localhost:3000"})

    # Send request with a valid header
    response = client.get("/hello-world", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == 'http://localhost:3000'
    
    # Send request with an invalid header
    response = client.get("/hello-world", headers={"Origin": "http://example.org"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") is None or response.headers.get("access-control-allow-origin") != "http://example.org"  
