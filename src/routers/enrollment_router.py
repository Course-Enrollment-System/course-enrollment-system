from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.enrollment import CourseEnrollment
from src.services.enrollment_services import EnrollmentService

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)

enrollment_service = EnrollmentService()

@router.post("/register")
def register_course(
    enrollment: CourseEnrollment,
    db: Session = Depends(get_db)
):
    try:
        return enrollment_service.register_course(db, enrollment)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/student/{student_id}")
def get_student_enrollments(
    student_id: int,
    db: Session = Depends(get_db)
):
    return enrollment_service.get_student_enrollments(db, student_id)