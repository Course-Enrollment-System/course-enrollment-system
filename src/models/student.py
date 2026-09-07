from pydantic import BaseModel, EmailStr
from typing import Optional
from src.models.role import Role


class Student(BaseModel):
    name: str
    email: EmailStr
    password: str
    department: str
    role: Role = Role.STUDENT