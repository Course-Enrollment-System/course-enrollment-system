from unittest.mock import Mock

import pytest

from src.models.student import Student
from src.services.student_service import StudentService


class TestStudentService:

    def test_create_student_with_existing_email(self):
        repository = Mock()
        db = Mock()

        repository.find_by_email.return_value = {
            "id": 1,
            "name": "Azeez Azeez",
            "email": "az@example.com",
            "department": "Biochemistry",
        }

        service = StudentService()
        service.student_repository = repository

        student = Student(
            name="Another Student",
            email="az@example.com",
            department="Biochemistry",
        )

        with pytest.raises(
            ValueError,
            match="Student with this email already exists",
        ):
            service.create_student(db, student)

        repository.create.assert_not_called()

    def test_create_student(self):
        repository = Mock()
        db = Mock()

        repository.find_by_email.return_value = None

        repository.create.return_value = {
            "id": 1,
            "name": "Azeez Azeez",
            "email": "az@example.com",
            "department": "Biochemistry",
        }

        service = StudentService()
        service.student_repository = repository

        student = Student(
            name="Azeez Azeez",
            email="az@example.com",
            department="Biochemistry",
        )

        result = service.create_student(db, student)

        assert result["name"] == "Azeez Azeez"
        assert result["email"] == "az@example.com"

        repository.find_by_email.assert_called_once_with(
            db,
            student.email,
        )

        repository.create.assert_called_once_with(
            db,
            student,
        )

    def test_get_student_by_id_not_found(self):
        repository = Mock()
        db = Mock()

        repository.find_by_id.return_value = None

        service = StudentService()
        service.student_repository = repository

        with pytest.raises(
            ValueError,
            match="Student not found",
        ):
            service.get_student_by_id(db, 999)

        repository.find_by_id.assert_called_once_with(
            db,
            999,
        )

    def test_get_student_by_id(self):
        repository = Mock()
        db = Mock()

        repository.find_by_id.return_value = {
            "id": 1,
            "name": "Azeez Azeez",
            "email": "az@example.com",
            "department": "Biochemistry",
        }

        service = StudentService()
        service.student_repository = repository

        result = service.get_student_by_id(db, 1)

        assert result["id"] == 1
        assert result["name"] == "Azeez Azeez"

        repository.find_by_id.assert_called_once_with(
            db,
            1,
        )

    def test_get_all_students(self):
        repository = Mock()
        db = Mock()

        repository.find_all.return_value = [
            {
                "id": 1,
                "name": "Azeez Azeez",
                "email": "az@example.com",
                "department": "Biochemistry",
            },
            {
                "id": 2,
                "name": "Emeka Dike",
                "email": "dicks@example.com",
                "department": "Computer Science",
            },
        ]

        service = StudentService()
        service.student_repository = repository

        result = service.get_all_students(db)

        assert len(result) == 2

        repository.find_all.assert_called_once_with(db)