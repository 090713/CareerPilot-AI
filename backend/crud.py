from sqlalchemy.orm import Session
from models import Student


def create_student(db: Session, name: str, email: str):
    student = Student(
        name=name,
        email=email
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def get_students(db: Session):
    return db.query(Student).all()


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(
        Student.id == student_id
    ).first()


def update_student(db: Session, student_id: int, name: str, email: str):

    student = get_student(db, student_id)

    if student:

        student.name = name
        student.email = email

        db.commit()
        db.refresh(student)

    return student


def delete_student(db: Session, student_id: int):

    student = get_student(db, student_id)

    if student:
        db.delete(student)
        db.commit()

    return student