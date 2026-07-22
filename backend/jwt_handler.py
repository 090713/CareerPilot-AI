"""
jwt_handler.py

Functions for creating JWT access tokens.
"""

import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import jwt

# =====================================================
# Load Environment Variables
# =====================================================

load_dotenv()

# Secret key used to sign JWT tokens
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY not found in .env file.")

# JWT Algorithm
ALGORITHM = "HS256"

# Token expiry time (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.

    Parameters:
        data (dict): Payload to include in the token.

    Returns:
        str: Encoded JWT token.
    """

    # Copy payload
    to_encode = data.copy()

    # Set expiration time
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Add expiry time to payload
    to_encode.update({"exp": expire})

    # Generate JWT token
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt