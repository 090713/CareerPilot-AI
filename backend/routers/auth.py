from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from security import verify_password
from jwt_handler import create_access_token
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
    login_data: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login using email and password.
    """

    student = crud.get_student_by_email(
        db,
        login_data.email
    )

    if student is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        login_data.password,
        student.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": student.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }