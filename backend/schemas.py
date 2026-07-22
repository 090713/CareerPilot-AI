from pydantic import BaseModel


# ==========================================
# Student Schemas
# ==========================================

class StudentCreate(BaseModel):
    name: str
    email: str
    password: str


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# ==========================================
# Authentication Schemas
# ==========================================

class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# ==========================================
# Job Schemas
# ==========================================

class JobCreate(BaseModel):
    job_title: str
    company: str
    description: str


# ==========================================
# Resume Response Schema
# ==========================================

class ResumeResponse(BaseModel):
    version: int
    filename: str
    resume_score: int | None = None
    uploaded_at: str | None = None


# ==========================================
# Job Match Response
# ==========================================

class JobMatchResponse(BaseModel):
    job_title: str
    company: str | None = None
    match_score: int
    matching_skills: list[str]
    missing_skills: list[str]
    recommendations: list[str]