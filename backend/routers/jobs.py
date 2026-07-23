from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from ai_service import match_resume_with_job
from database import get_db
from dependencies import get_current_user

# ==========================================
# Job Router
# ==========================================

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# ==========================================
# Upload Job Description
# ==========================================
@router.post("/upload")
def upload_job(
    job: schemas.JobCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a new job description.
    """

    # Logged-in student
    student = current_user

    # Save job description
    new_job = crud.create_job(
        db=db,
        student_id=student.id,
        job_title=job.job_title,
        company=job.company,
        description=job.description
    )

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
# Match Resume with Latest Job
# ==========================================
@router.post("/match")
def match_job(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Compare the latest uploaded resume with the latest job description.
    """

    # Logged-in student
    student = current_user

    # Latest Resume
    resume = crud.get_latest_resume(
        db,
        student.id
    )

    if resume is None:
        raise HTTPException(
            status_code=400,
            detail="No resume uploaded."
        )

    # Latest Job
    job = crud.get_latest_job(
        db,
        student.id
    )

    if job is None:
        raise HTTPException(
            status_code=400,
            detail="No job description uploaded."
        )

    # AI Matching
    result = match_resume_with_job(
        resume.resume_text,
        job.description
    )

    return {
        "success": True,
        "message": "Resume matched successfully.",
        "data": {
            "job_title": job.job_title,
            "company": job.company,
            **result
        }
    }