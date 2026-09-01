from sqlalchemy import Column, Integer, String, Text

from src.config.database import Base



class CourseModel(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    credit_unit = Column(Integer, nullable=False)
    department = Column(String(255), nullable=False)