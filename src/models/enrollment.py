from pydantic import BaseModel

class Enrollment(BaseModel):
    student_id: int
    session: str
    semester: str