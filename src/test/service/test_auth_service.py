from unittest.mock import Mock

import pytest

from src.models.admin import Admin
from src.models.student import Student
from src.services.auth_service import AuthService


class TestAuthService:

    def test_register_student_with_existing_email(self):
        repository = Mock()
        db = Mock()

        repository.find_by_email.return_value = {
            "id": 1,
            "name": "Azeez Azeez",
            "email": "az@example.com",
            "department": "Biochemistry",
        }

        service = AuthService()
        service.student_repository = repository

        student = Student(
            name="Another Student",
            email="az@example.com",
            department="Biochemistry",
            password="123456",
        )

        with pytest.raises(
            ValueError,
            match="Student with this email already exists",
        ):
            service.register_student(db, student)

        repository.create.assert_not_called()

    def test_register_student(self):
        repository = Mock()
        db = Mock()

        repository.find_by_email.return_value = None

        repository.create.return_value = {
            "id": 1,
            "name": "Azeez Azeez",
            "email": "az@example.com",
            "department": "Biochemistry",
        }

        service = AuthService()
        service.student_repository = repository

        student = Student(
            name="Azeez Azeez",
            email="az@example.com",
            department="Biochemistry",
            password="123456",
        )

        result = service.register_student(db, student)

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

    def test_register_admin_with_existing_email(self):
        repository = Mock()
        db = Mock()

        repository.find_by_email.return_value = {
            "id": 1,
            "name": "Admin",
            "email": "admin@yahoo.com",
        }

        service = AuthService()
        service.admin_repository = repository

        admin = Admin(
            name="Another Admin",
            email="admin@yahoo.com",
            password="123456",
        )

        with pytest.raises(
            ValueError,
            match="Admin with this email already exists",):
            service.register_admin(db, admin)

        repository.create.assert_not_called()

    def test_register_admin(self):
        repository = Mock()
        db = Mock()

        repository.find_by_email.return_value = None

        repository.create.return_value = {
            "id": 1,
            "name": "Admin",
            "email": "admin@yahoo.com",
        }

        service = AuthService()
        service.admin_repository = repository

        admin = Admin(
            name="Admin",
            email="admin@yahoo.com",
            password="123456",
        )

        result = service.register_admin(db, admin)

        assert result["name"] == "Admin"
        assert result["email"] == "admin@yahoo.com"

        repository.find_by_email.assert_called_once_with(
            db,
            admin.email,
        )

        repository.create.assert_called_once_with(
            db,
            admin,
        )

    def test_login_student(self):
        repository = Mock()
        db = Mock()

        repository.find_by_email.return_value = Mock(
            id=1,
            name="Azeez Azeez",
            email="az@example.com",
            department="Biochemistry",
            password="123456",
        )

        service = AuthService()
        service.student_repository = repository

        result = service.login_student(
            db,
            "az@example.com",
            "123456",
        )

        assert result["id"] == 1
        assert result["department"] == "Biochemistry"


        repository.find_by_email.assert_called_once_with(
            db,
            "az@example.com",
        )

    def test_login_admin(self):
        repository = Mock()
        db = Mock()

        repository.find_by_email.return_value = Mock(
            id=1,
            name="Admin",
            email="admin@yahoo.com",
            password="123456",
        )

        service = AuthService()
        service.admin_repository = repository

        result = service.login_admin(
            db,
            "admin@yahoo.com",
            "123456",
        )

        assert result["email"] == "admin@yahoo.com"
        assert result["role"] == "admin"


        repository.find_by_email.assert_called_once_with(
            db,
            "admin@yahoo.com",
        )

    def test_login_student_with_wrong_password(self):
        repository = Mock()
        db = Mock()

        repository.find_by_email.return_value = Mock(
            id=1,
            name="Azeez Azeez",
            email="az@example.com",
            department="Biochemistry",
            password="123456",
        )

        service = AuthService()
        service.student_repository = repository

        with pytest.raises(
            ValueError,
            match="Invalid password",
        ):
            service.login_student(
                db,
                "az@example.com",
                "wrongpassword",
            )

    def test_login_admin_with_wrong_password(self):
        repository = Mock()
        db = Mock()

        repository.find_by_email.return_value = Mock(
            id=1,
            name="Admin",
            email="admin@yahoo.com",
            password="123456",
        )

        service = AuthService()
        service.admin_repository = repository

        with pytest.raises(
            ValueError,
            match="Invalid email or password",
        ):
            service.login_admin(
                db,
                "admin@yahoo.com",
                "wrongpassword",
            )

    def test_login_student_not_found(self):
        repository = Mock()
        db = Mock()

        repository.find_by_email.return_value = None

        service = AuthService()
        service.student_repository = repository

        with pytest.raises(
            ValueError,
            match="Invalid password",
        ):
            service.login_student(
                db,
                "missing@example.com",
                "123456",
            )

    def test_login_admin_not_found(self):
        repository = Mock()
        db = Mock()

        repository.find_by_email.return_value = None

        service = AuthService()
        service.admin_repository = repository

        with pytest.raises(
            ValueError,
            match="Invalid email or password",
        ):
            service.login_admin(
                db,
                "missing@yahoo.com",
                "123456",
            )

    def test_logout(self):
        service = AuthService()

        result = service.logout()

        assert result["message"] == "Logged out successfully"