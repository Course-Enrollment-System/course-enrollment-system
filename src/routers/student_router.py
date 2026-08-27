from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.database import SessionLocal
from src.models.student import Student
from src.services.student_service import StudentService

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

student_service = StudentService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create_student")
def create_student(
    student: Student,
    db: Session = Depends(get_db)
):
    try:
        return student_service.create_student(db, student)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/get_student/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    try:
        return student_service.get_student_by_id(db, student_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get("/get_all_students")
def get_all_students(
    db: Session = Depends(get_db)
):
    return student_service.get_all_students(db)