from sqlalchemy import Column, ForeignKey, Integer, String

from src.config.database import Base


class EnrollmentModel(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    semester = Column(String(50), nullable=False)
    session = Column(String(20), nullable=False)