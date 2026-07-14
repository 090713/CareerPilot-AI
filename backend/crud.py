from sqlalchemy.orm import Session

import models
import schemas
from security import hash_password


# ==========================================
# CREATE a new student
# ==========================================
def create_student(db: Session, student: schemas.StudentCreate):
    # Debugging
    print("Password:", student.password)
    print("Type:", type(student.password))
    print("Length:", len(student.password))

    hashed_password = hash_password(student.password)

    db_student = models.Student(
        name=student.name,
        email=student.email,
        password=hashed_password
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student

def get_student_by_email(
    db: Session,
    email: str
):
    """
    Find a student using their email address.
    """

    return db.query(
        models.Student
    ).filter(
        models.Student.email == email
    ).first()


# ==========================================
# READ all students
# ==========================================
def get_students(db: Session):
    """
    Fetch all students from the database.
    """
    return db.query(models.Student).all()


# ==========================================
# READ one student by ID
# ==========================================
def get_student(db: Session, student_id: int):
    """
    Fetch a single student using their ID.
    Returns None if the student does not exist.
    """
    return db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()


# ==========================================
# UPDATE student details
# ==========================================
def update_student(db: Session, student_id: int, name: str, email: str):
    """
    Update a student's name and email.
    """

    # Find the student first
    student = get_student(db, student_id)

    # If student exists, update the details
    if student:
        student.name = name
        student.email = email

        # Save changes
        db.commit()

        # Refresh object with latest database values
        db.refresh(student)

    # Return updated student (or None if not found)
    return student


# ==========================================
# DELETE a student
# ==========================================
def delete_student(db: Session, student_id: int):
    """
    Delete a student using their ID.
    """

    # Find the student first
    student = get_student(db, student_id)

    # Delete only if the student exists
    if student:
        db.delete(student)
        db.commit()

    # Return deleted student (or None if not found)
    return student