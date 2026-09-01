from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.database import SessionLocal
from src.models.course import Course
from src.services.course_service import CourseService

router = APIRouter(
    prefix="/courses",
    tags=["Course"]
)

course_service = CourseService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create_course")
def create_course(
    course: Course,
    db: Session = Depends(get_db)
):
    try:
        return course_service.create_course(db, course)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )