from pydantic import BaseModel, EmailStr
from src.models.role import Role


class Student(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    department: str
    role: Role = Role.STUDENT