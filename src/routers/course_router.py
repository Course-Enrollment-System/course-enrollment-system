from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from src.config.database import get_db
from src.models.course import Course
from src.services.course_service import CourseService
from src.services.auth_state import AuthState


router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

course_service = CourseService()


@router.post("/create_course")
def create_course(
    course: Course,
    db: Session = Depends(get_db)
):
    current_user = AuthState.get_current_user()

    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="You're not logged in"
        )

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can create courses"
        )

    try:
        return course_service.create_course(
            db,
            course
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/get_all_courses")
def get_all_courses(
    db: Session = Depends(get_db)
):
    return course_service.find_all(db)


@router.get("/{code}")
def get_course(
    code: str,
    db: Session = Depends(get_db)
):
    try:
        return course_service.find_by_code(
            db,
            code
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.delete("/{code}")
def delete_course(code: str, db: Session = Depends(get_db)):

    current_user = AuthState.get_current_user()

    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Please login first"
        )

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete courses"
        )
    try:
        return course_service.delete_by_curse_code(db, code)

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Course does not exist"
        )