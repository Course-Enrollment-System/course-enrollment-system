from pydantic import ValidationError
import pytest

from src.models.student import Student

class TestStudent:

    def test_create_student(self):
        student = Student(
            name="Az",
            email="az@example.com",
            department="Biochemistry",
            password="123456"
        )

        assert student.name == "Az"
        assert student.email == "az@example.com"
        assert student.department == "Biochemistry"

    def test_student_requires_name(self):
        with pytest.raises(ValidationError):
            Student(
                email="az@example.com",
                department="Biochemistry"
            )

    def test_student_requires_email(self):
        with pytest.raises(ValidationError):
            Student(
                name="Az",
                department="Biochemistry"
            )

    def test_student_requires_department(self):
        with pytest.raises(ValidationError):
            Student(
                name="Az",
                email="az@example.com"
            )