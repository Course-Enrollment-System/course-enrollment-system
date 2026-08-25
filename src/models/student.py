from pydantic import BaseModel, EmailStr


class Student(BaseModel):
    name: str
    email: EmailStr
    department: str