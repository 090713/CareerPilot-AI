from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os

import crud
from database import get_db
from dependencies import get_current_user
from utils import extract_text_from_pdf
from ai_service import analyze_resume

# =====================================================
# Resume Router
# Handles Resume Upload, Analysis and Version History
# =====================================================

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

# Folder where uploaded resumes are stored
UPLOAD_FOLDER = "../uploads"

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =====================================================
# Upload Resume
# =====================================================
@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a PDF resume.

    Steps:
    1. Validate PDF
    2. Save PDF
    3. Extract text
    4. Store as a new resume version
    """

    # Allow only PDF files
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Save uploaded file
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)

    # Get logged-in student
    student = crud.get_student_by_email(
        db,
        current_user["sub"]
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    # Save as a new resume version
    new_resume = crud.create_resume(
        db=db,
        student_id=student.id,
        filename=file.filename,
        resume_text=extracted_text
    )

    return {
        "success": True,
        "message": "Resume uploaded successfully.",
        "data": {
            "student": student.name,
            "version": new_resume.version,
            "filename": new_resume.filename,
            "preview": extracted_text[:500]
        }
    }


# =====================================================
# Analyze Latest Resume
# =====================================================
@router.post("/analyze")
def analyze_uploaded_resume(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze the latest uploaded resume using Gemini AI.
    """

    # Get logged-in student
    student = crud.get_student_by_email(
        db,
        current_user["sub"]
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    # Get latest uploaded resume
    latest_resume = crud.get_latest_resume(
        db,
        student.id
    )

    if latest_resume is None:
        raise HTTPException(
            status_code=400,
            detail="No resume uploaded."
        )

    # Analyze resume using AI
    analysis = analyze_resume(
        latest_resume.resume_text
    )

    # Store analysis result in database
    latest_resume.analysis = str(analysis)

    if "resume_score" in analysis:
        latest_resume.resume_score = analysis["resume_score"]

    db.commit()

    return {
        "success": True,
        "message": "Resume analyzed successfully.",
        "data": {
            "student": student.name,
            "version": latest_resume.version,
            "resume_filename": latest_resume.filename,
            **analysis
        }
    }


# =====================================================
# Resume Version History
# =====================================================
@router.get("/history")
def get_resume_history(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Return all uploaded resume versions.
    """

    student = crud.get_student_by_email(
        db,
        current_user["sub"]
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    resumes = crud.get_resume_history(
        db,
        student.id
    )

    return {
        "success": True,
        "data": [
            {
                "version": resume.version,
                "filename": resume.filename,
                "resume_score": resume.resume_score,
                "uploaded_at": resume.uploaded_at,
                "is_current": resume.is_current
            }
            for resume in resumes
        ]
    }


# =====================================================
# Get Specific Resume Version
# =====================================================
@router.get("/version/{version}")
def get_resume_version(
    version: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetch a specific resume version.
    """

    student = crud.get_student_by_email(
        db,
        current_user["sub"]
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    resume = crud.get_resume_by_version(
        db,
        student.id,
        version
    )

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume version not found."
        )

    return {
        "success": True,
        "data": {
            "version": resume.version,
            "filename": resume.filename,
            "resume_score": resume.resume_score,
            "analysis": resume.analysis,
            "resume_text": resume.resume_text,
            "uploaded_at": resume.uploaded_at,
            "is_current": resume.is_current
        }
    }