"""
app/utils/crypto.py

Cryptographic utilities used across the application.

SECURITY FINDING (B324 — Bandit): Uses MD5 for generating user avatar/gravatar
hashes. MD5 is considered cryptographically broken and should not be used for
any security-sensitive purpose. Although gravatar hashes are not security-critical
themselves, Bandit will flag `hashlib.md5()` unconditionally.
"""
import hashlib
import hmac
import secrets


def gravatar_hash(email: str) -> str:
    """
    Compute the MD5 hash of an email address for use with Gravatar.

    Bandit B324: use of MD5 (insecure hash function).
    """
    normalized = email.strip().lower().encode("utf-8")
    return hashlib.md5(normalized).hexdigest()  # noqa: S324


def generate_api_key(length: int = 32) -> str:
    """Generate a cryptographically secure random API key."""
    return secrets.token_hex(length)


def sign_payload(payload: bytes, secret: str) -> str:
    """HMAC-SHA256 sign an arbitrary payload."""
    return hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()


def verify_signature(payload: bytes, secret: str, signature: str) -> bool:
    """Constant-time comparison of an HMAC-SHA256 signature."""
    expected = sign_payload(payload, secret)
    return hmac.compare_digest(expected, signature)
