from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
_SECRET = "super-secret-key"  # for assignment only; keep secret in env in real deployments
ALGORITHM = "HS256"

# Hardcoded users: username -> dict(password, role)
USERS = {
    "admin": {"password": "adminPass", "role": "admin"},
    "user": {"password": "userPass", "role": "user"}
}

class LoginIn(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: int

security = HTTPBearer()

def create_token(username: str, role: str, expires_seconds: int = 3600) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "sub": username,
        "role": role,
        "iat": now,
        "exp": now + datetime.timedelta(seconds=expires_seconds)
    }
    token = jwt.encode(payload, _SECRET, algorithm=ALGORITHM)
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, _SECRET, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    payload = verify_token(token)
    return payload

def require_role(role: str):
    def _require(payload=Depends(get_current_user)):
        if payload.get("role") != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden: insufficient role")
        return payload
    return _require

@router.get("/admin/protected", dependencies=[Depends(require_role("admin"))])
def admin_protected_route():
    """
    An endpoint accessible only to users with the 'admin' role.
    """
    return {"message": "Access granted to Admin user."}

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn):
    user = USERS.get(payload.username)
    if not user or user["password"] != payload.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_token(payload.username, user["role"], expires_seconds=3600)
    exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60)
    return {"access_token": token, "expires_at": int(exp.timestamp())}

@router.get("/validate")
def validate(payload=Depends(get_current_user)):
    # returns user details from token
    return {"user": payload.get("sub"), "role": payload.get("role")}
