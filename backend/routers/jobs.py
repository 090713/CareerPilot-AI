from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from ai_service import match_resume_with_job
from database import get_db
from dependencies import get_current_user

# Create a router for all Job-related APIs
router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# ==========================================
# Upload a Job Description
# ==========================================
@router.post("/upload")
def upload_job(
    job: schemas.JobCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get the logged-in student
    student = crud.get_student_by_email(
        db,
        current_user["sub"]
    )

    # Check whether the student exists
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    # Save the job description into the database
    new_job = crud.create_job(
        db=db,
        student_id=student.id,
        job_title=job.job_title,
        company=job.company,
        description=job.description
    )

    # Return success response
    return {
        "success": True,
        "message": "Job description uploaded successfully.",
        "data": {
            "job_id": new_job.id,
            "job_title": new_job.job_title,
            "company": new_job.company
        }
    }


# ==========================================
# Match Resume with Latest Job Description
# ==========================================
@router.post("/match")
def match_job(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get the logged-in student
    student = crud.get_student_by_email(
        db,
        current_user["sub"]
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    # Fetch the student's latest uploaded resume
    resume = crud.get_latest_resume(
        db,
        student.id
    )

    if resume is None:
        raise HTTPException(
            status_code=400,
            detail="No resume uploaded."
        )

    # Fetch the latest uploaded job description
    job = crud.get_latest_job(
        db,
        student.id
    )

    if job is None:
        raise HTTPException(
            status_code=400,
            detail="No job description uploaded."
        )

    # Use Gemini AI to compare the resume with the job description
    result = match_resume_with_job(
        resume.resume_text,
        job.description
    )

    # Return AI matching results
    return {
        "success": True,
        "message": "Resume matched successfully.",
        "data": {
            "job_title": job.job_title,
            "company": job.company,
            **result
        }
    }