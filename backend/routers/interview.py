from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import json
import crud
from ai_service import generate_interview_questions
from database import get_db
from dependencies import get_current_user

router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)


@router.post("/generate")
def generate_interview(
    db: Session = Depends(get_db),
    current_student=Depends(get_current_user)
):
    """
    Generate interview questions from the latest
    resume and job description.
    """

    latest_resume = crud.get_latest_resume(
        db,
        current_student.id
    )

    if not latest_resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    latest_job = crud.get_latest_job(
        db,
        current_student.id
    )

    if not latest_job:
        raise HTTPException(
            status_code=404,
            detail="Job description not found."
        )

    interview = generate_interview_questions(
        latest_resume.resume_text,
        latest_job.description
    )

    crud.save_interview(
        db=db,
        student_id=current_student.id,
        resume_id=latest_resume.id,
        job_id=latest_job.id,
        questions=json.dumps(interview)
    )

    return interview


@router.get("/history")
def interview_history(
    db: Session = Depends(get_db),
    current_student=Depends(get_current_user)
):
    """
    Return all previous interview sessions.
    """

    return crud.get_interviews(
        db,
        current_student.id
    )