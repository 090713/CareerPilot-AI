from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import schemas
from auth import create_access_token
from security import verify_password
from database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=schemas.Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login using email and password.
    """

    # Find student by email
    student = crud.get_student_by_email(
    db,
    form_data.username
)

    # Email not found
    if student is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Wrong password
    if not verify_password(
    form_data.password,
    student.password
):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": student.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }