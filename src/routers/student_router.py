from fastapi import APIRouter

from src.models.student import Student
from src.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["Students"])

student_service = StudentService()


@router.post("/create_student")
def create_student(student: Student):
    return student_service.create_student(student)


@router.get("/{student_id}")
def get_student(student_id: str):
    return student_service.get_student_by_id(student_id)


@router.get("/")
def get_all_students():
    return student_service.get_all_students()

