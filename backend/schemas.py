from pydantic import BaseModel


# ==========================
# Request Schema
# Used when creating a student
# ==========================
class StudentCreate(BaseModel):
    name: str
    email: str
    password: str


# ==========================
# Response Schema
# Used when sending data back
# Password is NOT returned
# ==========================
class StudentResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

# ==========================
# Login Request
# ==========================
class LoginRequest(BaseModel):
    email: str
    password: str


# ==========================
# Login Response
# ==========================
class Token(BaseModel):
    access_token: str
    token_type: str