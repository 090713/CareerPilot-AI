"""
auth.py

Functions for creating JWT access tokens.
"""

from datetime import datetime, timedelta
from jose import jwt

# Secret key (change this in production)
SECRET_KEY = "careerpilot_secret_key"

# JWT Algorithm
ALGORITHM = "HS256"

# Token expiry time
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """
    Create a JWT access token.
    """

    # Copy the payload
    to_encode = data.copy()

    # Set expiry time
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Add expiry to payload
    to_encode.update(
        {"exp": expire}
    )

    # Generate token
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt