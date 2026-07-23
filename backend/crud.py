from sqlalchemy.orm import Session

import models
import schemas
from security import hash_password


# ==========================================
# STUDENT CRUD
# ==========================================

def create_student(db: Session, student: schemas.StudentCreate):
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
    return (
        db.query(models.Student)
        .filter(models.Student.email == email)
        .first()
    )


def get_students(db: Session):
    return db.query(models.Student).all()


def get_student(
    db: Session,
    student_id: int
):
    return (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )


def update_student(
    db: Session,
    student_id: int,
    name: str,
    email: str
):
    student = get_student(db, student_id)

    if student:
        student.name = name
        student.email = email

        db.commit()
        db.refresh(student)

    return student


def delete_student(
    db: Session,
    student_id: int
):
    student = get_student(db, student_id)

    if student:
        db.delete(student)
        db.commit()

    return student


# ==========================================
# RESUME CRUD
# ==========================================

def get_latest_resume(
    db: Session,
    student_id: int
):
    return (
        db.query(models.Resume)
        .filter(
            models.Resume.student_id == student_id,
            models.Resume.is_current == 1
        )
        .first()
    )


def get_next_resume_version(
    db: Session,
    student_id: int
):
    latest = (
        db.query(models.Resume)
        .filter(
            models.Resume.student_id == student_id
        )
        .order_by(models.Resume.version.desc())
        .first()
    )

    if latest:
        return latest.version + 1

    return 1


def deactivate_current_resume(
    db: Session,
    student_id: int
):
    current = get_latest_resume(
        db,
        student_id
    )

    if current:
        current.is_current = 0
        db.commit()


def create_resume(
    db: Session,
    student_id: int,
    filename: str,
    resume_text: str
):
    version = get_next_resume_version(
        db,
        student_id
    )

    deactivate_current_resume(
        db,
        student_id
    )

    resume = models.Resume(
        student_id=student_id,
        version=version,
        filename=filename,
        resume_text=resume_text,
        is_current=1
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def get_resume_history(
    db: Session,
    student_id: int
):
    return (
        db.query(models.Resume)
        .filter(
            models.Resume.student_id == student_id
        )
        .order_by(models.Resume.version.desc())
        .all()
    )


def get_resume_by_version(
    db: Session,
    student_id: int,
    version: int
):
    return (
        db.query(models.Resume)
        .filter(
            models.Resume.student_id == student_id,
            models.Resume.version == version
        )
        .first()
    )


# ==========================================
# JOB CRUD
# ==========================================

def create_job(
    db: Session,
    student_id: int,
    job_title: str,
    company: str,
    description: str
):
    job = models.Job(
        student_id=student_id,
        job_title=job_title,
        company=company,
        description=description
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_latest_job(
    db: Session,
    student_id: int
):
    return (
        db.query(models.Job)
        .filter(
            models.Job.student_id == student_id
        )
        .order_by(models.Job.uploaded_at.desc())
        .first()
    )

# =====================================================
# Interview CRUD Operations
# =====================================================

def save_interview(
    db,
    student_id,
    resume_id,
    job_id,
    questions
):
    """
    Save an AI-generated interview session.
    """

    interview = models.Interview(
        student_id=student_id,
        resume_id=resume_id,
        job_id=job_id,
        questions=questions
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    return interview


def get_interviews(db, student_id):
    """
    Retrieve all interview sessions for a student.
    """

    return (
        db.query(models.Interview)
        .filter(models.Interview.student_id == student_id)
        .order_by(models.Interview.created_at.desc())
        .all()
    )