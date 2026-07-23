from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import crud
from database import get_db
from jwt_handler import verify_token

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Verify JWT token and return the current student.
    """

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    email = payload.get("sub")

    student = crud.get_student_by_email(
        db,
        email
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    return student