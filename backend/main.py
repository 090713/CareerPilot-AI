from fastapi import FastAPI

# Middleware used to allow the React frontend
# to communicate with the FastAPI backend.
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base

# Import all API routers
from routers import students
from routers import auth
from routers import resume
from routers import jobs
from routers import interview

# =====================================================
# Create Database Tables
# =====================================================
# This creates all tables defined in models.py
# if they don't already exist.
Base.metadata.create_all(bind=engine)

# =====================================================
# Create FastAPI Application
# =====================================================
app = FastAPI(
    title="CareerPilot AI",
    description="AI-powered Career Guidance Platform using FastAPI, PostgreSQL and Gemini AI",
    version="2.0.0"
)

# =====================================================
# CORS Configuration
# =====================================================
# CORS (Cross-Origin Resource Sharing) allows the React
# frontend running on a different port to access this
# FastAPI backend.

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,

    # Allow requests only from the frontend URLs above
    allow_origins=origins,

    # Allow cookies and authentication headers
    allow_credentials=True,

    # Allow all HTTP methods (GET, POST, PUT, DELETE...)
    allow_methods=["*"],

    # Allow all request headers
    allow_headers=["*"],
)

# =====================================================
# Register API Routers
# =====================================================

# Student Management APIs
app.include_router(students.router)

# Authentication APIs
app.include_router(auth.router)

# Resume APIs
app.include_router(resume.router)

# Job Description APIs
app.include_router(jobs.router)

# Interview Schema APIs
app.include_router(interview.router)


# =====================================================
# Home Endpoint
# =====================================================
@app.get("/")
def home():
    """
    Root endpoint of the application.
    """

    return {
        "message": "Welcome to CareerPilot AI 🚀",
        "version": "2.0.0"
    }


# =====================================================
# About Endpoint
# =====================================================
@app.get("/about")
def about():
    """
    Returns project information.
    """

    return {
        "project": "CareerPilot AI",
        "developer": "Mahitha",
        "framework": "FastAPI",
        "database": "PostgreSQL",
        "ai_model": "Google Gemini"
    }


# =====================================================
# Health Check Endpoint
# =====================================================
@app.get("/health")
def health():
    """
    Used to verify whether the backend is running.
    """

    return {
        "status": "Healthy",
        "message": "CareerPilot AI Backend is running successfully."
    }