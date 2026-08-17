import jwt  # PyJWT
import hashlib  # ruff: unused import (intentional)
import os       # ruff: unused import (intentional)
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Bandit finding: hardcoded-secret (B105)
SECRET_KEY = "orbitboard-dev-secret-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    """
    Decode and validate a JWT token.

    SECURITY BUG: This function intentionally does NOT wrap jwt.decode() in a
    try/except block. If the token is malformed, expired, or has an invalid
    signature, jwt.decode() raises jwt.DecodeError or jwt.ExpiredSignatureError.
    These are NOT caught here, so they bubble up as an unhandled 500 Server Error
    instead of a graceful 401 Unauthorized response.
    """
    # Bug: no try/except — jwt.DecodeError or jwt.ExpiredSignatureError propagates uncaught
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


def get_current_user_id(token: str) -> int:
    """Extract user_id from a verified token. Crashes on bad token (see verify_token)."""
    payload = verify_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise ValueError("Token payload missing 'sub' field")
    return int(user_id)

