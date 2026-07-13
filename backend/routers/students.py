from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Import database dependency
from database import get_db

# Import request schema
from schemas import StudentCreate

# Import CRUD functions
import crud


# Create a router for all student-related APIs
router = APIRouter(
    prefix="/students",      # All routes start with /students
    tags=["Students"]        # Group these endpoints in Swagger UI
)


# ==========================
# CREATE STUDENT
# ==========================
@router.post("/")
def register_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new student in the database.
    """

    new_student = crud.create_student(
        db,
        student.name,
        student.email
    )

    return {
        "message": "Student Registered Successfully!",
        "student": new_student
    }


# ==========================
# GET ALL STUDENTS
# ==========================
@router.get("/")
def get_students(
    db: Session = Depends(get_db)
):
    """
    Fetch all students from the database.
    """

    return crud.get_students(db)


# ==========================
# GET STUDENT BY ID
# ==========================
@router.get("/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Fetch one student using their ID.
    """

    student = crud.get_student(db, student_id)

    if not student:
        return {"message": "Student not found"}

    return student


# ==========================
# UPDATE STUDENT
# ==========================
@router.put("/{student_id}")
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    """
    Update a student's information.
    """

    updated = crud.update_student(
        db,
        student_id,
        student.name,
        student.email
    )

    if not updated:
        return {"message": "Student not found"}

    return {
        "message": "Student Updated Successfully!",
        "student": updated
    }


# ==========================
# DELETE STUDENT
# ==========================
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a student from the database.
    """

    deleted = crud.delete_student(db, student_id)

    if not deleted:
        return {"message": "Student not found"}

    return {
        "message": "Student Deleted Successfully!"
    }