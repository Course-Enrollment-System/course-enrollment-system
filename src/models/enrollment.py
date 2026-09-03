from pydantic import BaseModel

class Enrollment(BaseModel):
    student_id: int
    course_code: str
    semester: str