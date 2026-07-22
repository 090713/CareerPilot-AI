from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base


class Student(Base):
    __tablename__ = "students"

    # Primary Key (Auto Increment ID)
    id = Column(Integer, primary_key=True, index=True)

    # Student Name
    name = Column(String, nullable=False)

    # Student Email (Must be unique)
    email = Column(String, unique=True, nullable=False)

    # Stores the HASHED password (Never store plain passwords)
    password = Column(String, nullable=False)

    resume_filename = Column(String, nullable=True)
    resume_text = Column(Text, nullable=True)

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    version = Column(
        Integer,
        nullable=False
    )

    filename = Column(
        String,
        nullable=False
    )

    resume_text = Column(
        Text,
        nullable=False
    )

    resume_score = Column(
        Integer,
        nullable=True
    )

    analysis = Column(
        Text,
        nullable=True
    )

    is_current = Column(
    Integer,
    default=1
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )