from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    email: str


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True