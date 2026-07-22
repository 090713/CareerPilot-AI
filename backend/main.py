from fastapi import FastAPI
from database import engine
from models import Base
from routers import students, auth
from routers import resume

# Create FastAPI application
app = FastAPI(
    title="CareerPilot AI",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include Student Router
app.include_router(students.router)
app.include_router(auth.router)
app.include_router(resume.router)

# Home Endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to CareerPilot AI!"
    }


# About Endpoint
@app.get("/about")
def about():
    return {
        "project": "CareerPilot AI",
        "developer": "Mahitha"
    }


# Health Check Endpoint
@app.get("/health")
def health():
    return {
        "status": "Server is running successfully"
    }