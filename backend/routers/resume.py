from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os

import crud
from database import get_db
from dependencies import get_current_user
from utils import extract_text_from_pdf
from ai_service import analyze_resume

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

UPLOAD_FOLDER = "../uploads"

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a PDF resume, save it, extract its text,
    and store the resume details in the database.
    """

    # Allow only PDF files
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Save uploaded PDF
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from the PDF
    extracted_text = extract_text_from_pdf(file_path)

    # Get logged-in student using email stored in JWT
    student = crud.get_student_by_email(
        db,
        current_user["sub"]
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    # Save resume information in the database
    crud.update_student_resume(
        db=db,
        student_id=student.id,
        filename=file.filename,
        resume_text=extracted_text
    )

    return {
        "message": "Resume uploaded successfully!",
        "student": student.name,
        "filename": file.filename,
        "preview": extracted_text[:500]
    }


@router.post("/analyze")
def analyze_uploaded_resume(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze the logged-in student's stored resume.
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

    # Check if a resume has been uploaded
    if not student.resume_text:
        raise HTTPException(
            status_code=400,
            detail="No resume uploaded."
        )

    analysis = analyze_resume(student.resume_text)
    return {
    "student": student.name,
    "resume_filename": student.resume_filename,
    **analysis
}