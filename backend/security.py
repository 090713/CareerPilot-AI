"""
security.py

Contains helper functions for:
1. Password hashing
2. Password verification
3. JWT token creation
4. JWT token verification
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# ==========================
# Password Hashing
# ==========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ==========================
# JWT Configuration
# ==========================

SECRET_KEY = "careerpilot_secret_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ==========================
# Password Functions
# ==========================

def hash_password(password: str):
    """
    Convert a plain password into a secure hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    Check whether the entered password matches the stored hash.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ==========================
# JWT Functions
# ==========================

def create_access_token(data: dict):
    """
    Create a JWT access token.
    """

    # Copy payload
    to_encode = data.copy()

    # Set token expiry time
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Add expiry to payload
    to_encode.update({"exp": expire})

    # Create JWT
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str):
    """
    Verify JWT token.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None