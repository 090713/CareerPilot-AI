from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base
from datetime import datetime


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

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


class Job(Base):
    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    job_title = Column(
        String,
        nullable=False
    )

    company = Column(
        String,
        nullable=True
    )

    description = Column(
        Text,
        nullable=False
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

# =====================================================
# Interview Model
# Stores AI-generated interview sessions
# =====================================================

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False
    )

    questions = Column(Text, nullable=False)

    created_at = Column(
    DateTime(timezone=True),
    server_default=func.now()
    )