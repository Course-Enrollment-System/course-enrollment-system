from pydantic import BaseModel


class Course(BaseModel):
    code: str
    title: str
    credit_unit: int
    department: str

