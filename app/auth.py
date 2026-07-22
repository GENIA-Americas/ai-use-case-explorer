"""
Admin-key protection for write operations.

This repo is different from the others in the toolkit: it's a shared
reference library (no org_name field anywhere — every other tool in the
toolkit is meant to read from this one shared set of use cases), not
per-org private data. So the fix here isn't per-org scoping, it's
write protection: reads (GET) stay fully open, since that's the whole
point of a shared reference library, but writes (POST, DELETE) need to
require an admin key, otherwise any anonymous caller on the public
internet can pollute or wipe the library every other tool depends on.

Keys are read from the ADMIN_API_KEYS env var as a comma-separated list
(no org mapping needed, since there's only one library, not one per org).
"""
import hmac
import os

from fastapi import Header, HTTPException, status


def _load_admin_keys() -> list[str]:
    raw = os.getenv("ADMIN_API_KEYS", "")
    return [k.strip() for k in raw.split(",") if k.strip()]


_ADMIN_KEYS = _load_admin_keys()

_UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or missing admin API key",
    headers={"WWW-Authenticate": "X-Admin-Key"},
)


def require_admin_key(x_admin_key: str | None = Header(None, alias="X-Admin-Key")) -> None:
    """
    FastAPI dependency for write endpoints only. Header is optional
    (default None) rather than required so a missing header and a wrong
    header both return the same 401, instead of FastAPI's own request
    validation intercepting a missing required header with a 422 before
    this code runs — same reasoning as the per-org auth in the other
    toolkit repos.
    """
    if x_admin_key is None:
        raise _UNAUTHORIZED

    for known_key in _ADMIN_KEYS:
        if hmac.compare_digest(x_admin_key, known_key):
            return

    raise _UNAUTHORIZED
