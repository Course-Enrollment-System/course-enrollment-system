from src.models.student import Student
from src.repositories.student_repository import StudentRepository


class StudentService:

    def __init__(self):
        self.student_repository = StudentRepository()

    def create_student(self, student: Student):
        return self.student_repository.create(student)

    def get_student_by_id(self, student_id: str):
        return self.student_repository.find_by_id(student_id)

    def get_all_students(self):
        return self.student_repository.find_all()