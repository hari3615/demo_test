"""
tests/unit/test_auth_service.py

Tests for authentication service.
Two passing tests for normal flow, one FAILING test for the JWT security bug.
"""
import pytest
from datetime import timedelta

from app.services import auth_service


# ── Passing tests ──────────────────────────────────────────────────────────────

def test_password_hashing_and_verification():
    """A correct password should pass verification."""
    raw = "super-secret-password"
    hashed = auth_service.get_password_hash(raw)
    assert auth_service.verify_password(raw, hashed)


def test_wrong_password_fails_verification():
    """A wrong password must NOT pass verification."""
    hashed = auth_service.get_password_hash("correct-horse-battery")
    assert not auth_service.verify_password("wrong-guess", hashed)


def test_create_and_verify_valid_token():
    """A freshly created token should decode successfully."""
    token = auth_service.create_access_token({"sub": "42"})
    payload = auth_service.verify_token(token)
    assert payload["sub"] == "42"


# ── Failing test ───────────────────────────────────────────────────────────────

def test_verify_token_with_malformed_token():
    """
    FAILS on HEAD.

    Supplying a malformed token to verify_token() should return a 401-style
    error. Instead, because verify_token() does NOT catch jwt.DecodeError,
    it raises an unhandled jwt.exceptions.DecodeError (a subclass of Exception),
    causing a 500 crash at the route level.

    This test calls the function directly and expects it to raise — the pipeline
    must fix auth_service.verify_token to catch jwt.DecodeError and raise
    HTTPException(401) (or equivalent) instead.
    """
    malformed_token = "not.a.valid.jwt.token"
    # The bug: jwt.DecodeError is NOT caught inside verify_token(), so it propagates raw.
    # This test will ERROR (not just FAIL) because the exception is unhandled.
    auth_service.verify_token(malformed_token)
