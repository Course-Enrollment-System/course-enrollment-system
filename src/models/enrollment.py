from typing import List
from pydantic import BaseModel
from src.models.semester import Semester

class CourseEnrollmentRequest(BaseModel):
    student_id: int
    semester: Semester
    session: str
    course_codes: List[str]