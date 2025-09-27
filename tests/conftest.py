import httpx
import pytest
from fastapi.testclient import TestClient
from main import app
from services import auth_service
import jwt
import datetime

client = TestClient(app)

@pytest.fixture
def test_client() -> httpx.Client:
    return client

@pytest.fixture
def admin_token() -> str:
    token = auth_service.create_token("admin", "admin", expires_seconds=3600)
    return token

@pytest.fixture
def user_token() -> str:
    token = auth_service.create_token("user", "user", expires_seconds=3600)
    return token

@pytest.fixture
def expired_token() -> str:
    """Create an expired token for testing"""
    token = auth_service.create_token("user", "user", expires_seconds=-1)
    return token

@pytest.fixture
def invalid_token() -> str:
    """Create an invalid token with wrong secret"""
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "sub": "user",
        "role": "user",
        "iat": now,
        "exp": now + datetime.timedelta(minutes=60)
    }
    # Use wrong secret to create invalid token
    token = jwt.encode(payload, "wrong-secret", algorithm="HS256")
    return token

@pytest.fixture
def malformed_token() -> str:
    """Return a malformed token string"""
    return "this.is.not.a.valid.jwt.token"
