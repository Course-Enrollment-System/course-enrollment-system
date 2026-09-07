from pydantic import BaseModel
from src.models.semester import Semester

class CourseEnrollment(BaseModel):
    student_id: int
    course_code: str
    session: str
    semester: Semester
