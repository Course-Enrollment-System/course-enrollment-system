import pytest

from config.database import students_collection
from src.models.student import Student
from src.repositories.student_repository import StudentRepository


class TestStudentRepository:

    @pytest.fixture
    def student_repository(self):
        return StudentRepository()

    @pytest.fixture(autouse=True)
    def clear_database(self):
        yield
        students_collection.delete_many({})

    def test_create_student(self, student_repository):
        student = Student(
            name="az",
            email="az@example.com",
            department="Biochemistry"
        )

        created_student = student_repository.create(student)

        assert created_student["name"] == "az"
        assert created_student["email"] == "az@example.com"
        assert created_student["department"] == "Biochemistry"
        assert created_student["id"] is not None


    def test_find_student_by_id(self, student_repository):
        student = Student(
        name="az",
        email="az@example.com",
        department="Biochemistry"
        )

        created_student = student_repository.create(student)

        found_student = student_repository.find_by_id(created_student["id"])

        assert found_student["id"] == created_student["id"]