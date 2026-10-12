"""Auth module: resolves the authenticated sales rep from a bearer token."""
from fastapi import Header, HTTPException

from . import data


def rep_from_token(token: str) -> str | None:
    return data.TOKENS.get(token)


def current_rep(authorization: str | None = Header(default=None)) -> str:
    """FastAPI dependency: returns the sales rep id or raises 401."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    rep = rep_from_token(authorization.removeprefix("Bearer ").strip())
    if rep is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return rep
