from unittest.mock import Mock

from src.models.student import Student
from src.services.student_service import StudentService


class TestStudentService:

    def test_create_student(self):
        repository = Mock()

        student = Student(
            name="az",
            email="az@example.com",
            department="Biochemistry"
        )

        repository.create.return_value = {
            "id": "123",
            "name": "az",
            "email": "az@example.com",
            "department": "Biochemistry"
        }

        service = StudentService()
        service.student_repository = repository

        result = service.create_student(student)

        assert result["name"] == "az"
        assert result["email"] == "az@example.com"

        repository.create.assert_called_once_with(student)


    def test_get_student_by_id(self):
        repository = Mock()

        repository.find_by_id.return_value = {
            "id": "123",
            "name": "az",
            "email": "az@example.com",
            "department": "Biochemistry"
        }

        service = StudentService()
        service.student_repository = repository

        result = service.get_student_by_id("123")

        assert result["name"] == "az"

        repository.find_by_id.assert_called_once_with("123")

    def test_get_all_students(self):
        repository = Mock()

        repository.find_all.return_value = [
            {
                "id": "123",
                "name": "az",
                "email": "az@example.com",
                "department": "Biochemistry"
            },
            {
                "id": "456",
                "name": "ab",
                "email": "ab@example.com",
                "department": "Biotechnology"
            }
        ]

        service = StudentService()
        service.student_repository = repository

        result = service.get_all_students()

        assert len(result) == 2


        repository.find_all.assert_called_once()