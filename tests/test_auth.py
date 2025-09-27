import time
import datetime
import pytest
import jwt
from services import auth_service
from main import app

# ============= Table-Driven Login Tests =============

@pytest.mark.parametrize("test_case", [
    # Success cases
    {
        "name": "admin_login_success",
        "username": "admin",
        "password": "adminPass",
        "expected_status": 200,
        "expected_role": "admin",
        "check_token": True
    },
    {
        "name": "user_login_success",
        "username": "user",
        "password": "userPass",
        "expected_status": 200,
        "expected_role": "user",
        "check_token": True
    },
    # Failure cases
    {
        "name": "wrong_password",
        "username": "admin",
        "password": "wrongPass",
        "expected_status": 401,
        "expected_detail": "Invalid credentials",
        "check_token": False
    },
    {
        "name": "non_existent_user",
        "username": "nonexistent",
        "password": "anypass",
        "expected_status": 401,
        "expected_detail": "Invalid credentials",
        "check_token": False
    },
    {
        "name": "empty_username",
        "username": "",
        "password": "adminPass",
        "expected_status": 401,
        "check_token": False
    },
    {
        "name": "empty_password",
        "username": "admin",
        "password": "",
        "expected_status": 401,  # Will pass validation but fail auth
        "expected_detail": "Invalid credentials",
        "check_token": False
    },
    {
        "name": "case_sensitive_username",
        "username": "Admin",  # Capital A
        "password": "adminPass",
        "expected_status": 401,
        "expected_detail": "Invalid credentials",
        "check_token": False
    },
    {
        "name": "sql_injection_attempt",
        "username": "admin' OR '1'='1",
        "password": "' OR '1'='1",
        "expected_status": 401,
        "expected_detail": "Invalid credentials",
        "check_token": False
    },
])
def test_login_scenarios(test_client, test_case):
    """Test various login scenarios using table-driven approach"""
    resp = test_client.post("/auth/login", json={
        "username": test_case["username"],
        "password": test_case["password"]
    })
    
    assert resp.status_code == test_case["expected_status"], f"Failed: {test_case['name']}"
    
    if test_case["expected_status"] == 200:
        body = resp.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"
        assert "expires_at" in body
        
        if test_case["check_token"]:
            # Decode and verify token content
            payload = jwt.decode(body["access_token"], auth_service._SECRET, algorithms=[auth_service.ALGORITHM])
            assert payload["sub"] == test_case["username"]
            assert payload["role"] == test_case["expected_role"]
            assert "exp" in payload
            assert "iat" in payload
    
    elif test_case["expected_status"] == 401:
        if "expected_detail" in test_case:
            assert test_case["expected_detail"] in resp.json().get("detail", "")


# ============= Table-Driven Token Validation Tests =============

@pytest.mark.parametrize("test_case", [
    {
        "name": "valid_admin_token",
        "token_fixture": "admin_token",
        "expected_status": 200,
        "expected_user": "admin",
        "expected_role": "admin"
    },
    {
        "name": "valid_user_token",
        "token_fixture": "user_token",
        "expected_status": 200,
        "expected_user": "user",
        "expected_role": "user"
    },
    {
        "name": "expired_token",
        "token_fixture": "expired_token",
        "expected_status": 401,
        "expected_detail": "Token expired"
    },
    {
        "name": "invalid_token",
        "token_fixture": "invalid_token",
        "expected_status": 401,
        "expected_detail": "Invalid token"
    },
    {
        "name": "malformed_token",
        "token_fixture": "malformed_token",
        "expected_status": 401,
        "expected_detail": "Invalid token"
    },
    {
        "name": "no_token",
        "token_fixture": None,
        "expected_status": 403,
        "expected_detail": "Not authenticated"
    },
    {
        "name": "empty_bearer",
        "token_fixture": "",
        "expected_status": 403,
        "expected_detail": "Not authenticated"
    },
])
def test_validate_token_scenarios(test_client, request, test_case):
    """Test various token validation scenarios"""
    headers = {}
    
    if test_case["token_fixture"] is not None:
        if test_case["token_fixture"]:  # Non-empty string
            token = request.getfixturevalue(test_case["token_fixture"]) if test_case["token_fixture"] != "" else ""
            headers = {"Authorization": f"Bearer {token}"}
        else:  # Empty string case
            headers = {"Authorization": "Bearer "}
    
    resp = test_client.get("/auth/validate", headers=headers)
    assert resp.status_code == test_case["expected_status"], f"Failed: {test_case['name']}"
    
    if test_case["expected_status"] == 200:
        data = resp.json()
        assert data["user"] == test_case["expected_user"]
        assert data["role"] == test_case["expected_role"]
    else:
        if "expected_detail" in test_case:
            assert test_case["expected_detail"] in resp.json().get("detail", "")


# ============= Protected Endpoint Tests (if you have role-based endpoints) =============

@pytest.mark.parametrize("test_case", [
    {
        "name": "admin_access_admin_endpoint",
        "endpoint": "/auth/admin/protected",  # Assuming you have this endpoint
        "token_fixture": "admin_token",
        "expected_status": 200
    },
    {
        "name": "user_access_admin_endpoint",
        "endpoint": "/auth/admin/protected",
        "token_fixture": "user_token",
        "expected_status": 403
    },
    {
        "name": "no_token_admin_endpoint",
        "endpoint": "/auth/admin/protected",
        "token_fixture": None,
        "expected_status": 403
    },
])
def test_role_based_access(test_client, request, test_case):
    """Test role-based access control"""
    # Skip if endpoint doesn't exist
    if not hasattr(app, 'routes'):
        pytest.skip("Endpoint not configured")
    
    headers = {}
    if test_case["token_fixture"]:
        token = request.getfixturevalue(test_case["token_fixture"])
        headers = {"Authorization": f"Bearer {token}"}
    
    # This assumes you have role-protected endpoints
    # Adjust the endpoint paths according to your actual implementation
    resp = test_client.get(test_case["endpoint"], headers=headers)
    
    assert resp.status_code == test_case["expected_status"], f"Failed: {test_case['name']}"


# ============= Edge Cases and Security Tests =============

def test_multiple_login_attempts(test_client):
    """Test multiple login attempts don't interfere with each other"""
    # First login
    resp1 = test_client.post("/auth/login", json={"username": "admin", "password": "adminPass"})
    token1 = resp1.json()["access_token"]
    
    # Second login same user
    time.sleep(1)
    resp2 = test_client.post("/auth/login", json={"username": "admin", "password": "adminPass"})
    token2 = resp2.json()["access_token"]
    
    # Both tokens should be valid but different
    assert token1 != token2
    
    # Both should validate successfully
    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}
    
    resp1_validate = test_client.get("/auth/validate", headers=headers1)
    resp2_validate = test_client.get("/auth/validate", headers=headers2)
    
    assert resp1_validate.status_code == 200
    assert resp2_validate.status_code == 200


def test_token_expiration_boundary(test_client):
    """Test token behavior at expiration boundary"""
    # Create token with 1 second expiry
    token = auth_service.create_token("user", "user", expires_seconds=1)  # 1 second
    headers = {"Authorization": f"Bearer {token}"}
    
    # Should work immediately
    resp = test_client.get("/auth/validate", headers=headers)
    assert resp.status_code == 200
    
    # Wait for expiration
    time.sleep(2)
    
    # Should fail after expiration
    resp = test_client.get("/auth/validate", headers=headers)
    assert resp.status_code == 401
    assert "Token expired" in resp.json()["detail"]


def test_concurrent_requests_same_token(test_client, user_token):
    """Test that the same token can be used for multiple concurrent requests"""
    headers = {"Authorization": f"Bearer {user_token}"}
    
    # Make multiple requests with same token
    responses = []
    for _ in range(5):
        resp = test_client.get("/auth/validate", headers=headers)
        responses.append(resp)
    
    # All should succeed
    for resp in responses:
        assert resp.status_code == 200
        assert resp.json()["user"] == "user"


def test_malformed_authorization_headers(test_client, user_token):
    """Test various malformed authorization headers"""
    test_cases = [
        {"header": f"Basic {user_token}", "name": "wrong_auth_type"},
        {"header": f"Bearer", "name": "missing_token"},
        {"header": f"Bearer  {user_token}", "name": "extra_spaces"},
        {"header": f"{user_token}", "name": "no_bearer_prefix"},
        {"header": f"Bearer {user_token} extra", "name": "extra_content"},
    ]
    
    for test_case in test_cases:
        headers = {"Authorization": test_case["header"]}
        resp = test_client.get("/auth/validate", headers=headers)
        # Most of these should return 403 (Not authenticated) or 401
        assert resp.status_code in [401, 403], f"Failed: {test_case['name']}"


def test_token_payload_integrity(test_client):
    """Test that token payload is preserved correctly"""
    resp = test_client.post("/auth/login", json={"username": "admin", "password": "adminPass"})
    token = resp.json()["access_token"]
    
    # Decode token and verify all expected fields
    payload = jwt.decode(token, auth_service._SECRET, algorithms=[auth_service.ALGORITHM])
    
    assert payload["sub"] == "admin"
    assert payload["role"] == "admin"
    assert "iat" in payload
    assert "exp" in payload
    
    # Verify exp is approximately 60 minutes from iat
    exp_time = datetime.datetime.fromtimestamp(payload["exp"], tz=datetime.timezone.utc)
    iat_time = datetime.datetime.fromtimestamp(payload["iat"], tz=datetime.timezone.utc)
    time_diff = exp_time - iat_time
    
    # Should be approximately 60 minutes (3600 seconds)
    assert 3595 <= time_diff.total_seconds() <= 3605


def test_login_response_format(test_client):
    """Test that login response conforms to expected format"""
    resp = test_client.post("/auth/login", json={"username": "user", "password": "userPass"})
    
    assert resp.status_code == 200
    body = resp.json()
    
    # Check all required fields
    assert "access_token" in body
    assert "token_type" in body
    assert "expires_at" in body
    
    # Check field types
    assert isinstance(body["access_token"], str)
    assert body["token_type"] == "bearer"
    assert isinstance(body["expires_at"], int)
    
    # Verify expires_at is a valid timestamp
    expires_at = datetime.datetime.fromtimestamp(body["expires_at"], tz=datetime.timezone.utc)
    now = datetime.datetime.now(datetime.timezone.utc)
    
    # Should be approximately 60 minutes in the future
    time_diff = expires_at - now
    assert 3595 <= time_diff.total_seconds() <= 3605
