from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from security import verify_token

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    """
    Verify JWT token and return current user.
    """

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload