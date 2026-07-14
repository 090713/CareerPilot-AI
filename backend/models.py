from sqlalchemy import Column, Integer, String
from database import Base


class Student(Base):
    __tablename__ = "students"

    # Primary Key (Auto Increment ID)
    id = Column(Integer, primary_key=True, index=True)

    # Student Name
    name = Column(String, nullable=False)

    # Student Email (Must be unique)
    email = Column(String, unique=True, nullable=False)

    # Stores the HASHED password (Never store plain passwords)
    password = Column(String, nullable=False)