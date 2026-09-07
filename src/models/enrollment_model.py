from sqlalchemy import Column, ForeignKey, Integer, String, Enum, UniqueConstraint
from src.config.database import Base
from src.models.semester import Semester

class EnrollmentModel(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_code = Column(String(100), ForeignKey("courses.code"), nullable=False)
    session = Column(String(50), nullable=False)
    semester = Column(Enum(Semester, native_enum=False), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "course_code",
            "session",
            "semester",
            name="uq_student_course_semester_session"
        ),
    )