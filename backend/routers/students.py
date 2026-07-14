from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db
from dependencies import get_current_user

# ==========================================
# Create Router
# All student-related APIs start with /students
# ==========================================
router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# ==========================================
# CREATE Student
# ==========================================
@router.post(
    "/",
    response_model=schemas.StudentResponse
)
def register_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new student.

    The password is automatically hashed
    before storing it in the database.
    """

    return crud.create_student(db, student)


# ==========================================
# GET All Students
# ==========================================
@router.get(
    "/",
    response_model=list[schemas.StudentResponse]
)
def get_students(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Retrieve all students.
    Only authenticated users can access this endpoint.
    """

    return crud.get_students(db)


# ==========================================
# GET Student by ID
# ==========================================
@router.get(
    "/{student_id}",
    response_model=schemas.StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Retrieve one student by ID.
    """

    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# ==========================================
# UPDATE Student
# ==========================================
@router.put(
    "/{student_id}",
    response_model=schemas.StudentResponse
)
def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Update student information.
    """

    updated_student = crud.update_student(
        db,
        student_id,
        student.name,
        student.email
    )

    if updated_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return updated_student


# ==========================================
# DELETE Student
# ==========================================
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Delete a student.
    """

    deleted_student = crud.delete_student(
        db,
        student_id
    )

    if deleted_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully."
    }