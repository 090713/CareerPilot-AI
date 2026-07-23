"""
security.py

Password hashing and password verification utilities.
"""

from passlib.context import CryptContext

# ==========================
# Password Hashing
# ==========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

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
