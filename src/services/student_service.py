from sqlalchemy.orm import Session

from src.models.student import Student
from src.repositories.student_repository import StudentRepository


class StudentService:

    def __init__(self):
        self.student_repository = StudentRepository()

    def create_student(self, db: Session, student: Student):

        existing_student = self.student_repository.find_by_email(
            db,
            student.email
        )

        if existing_student:
            raise ValueError("Student with this email already exists")

        return self.student_repository.create(db, student)

    def get_student_by_id(self, db: Session, student_id: int):

        student = self.student_repository.find_by_id(db, student_id)

        if student is None:
            raise ValueError("Student not found")

        return student

    def get_all_students(self, db: Session):

        return self.student_repository.find_all(db)