from sqlalchemy.orm import Session

from src.models.student import Student
from src.models.admin import Admin
from src.repositories.student_repository import StudentRepository
from src.repositories.admin_repository import AdminRepository
from src.services.auth_state import AuthState


class AuthService:

    def __init__(self):
        self.student_repository = StudentRepository()
        self.admin_repository = AdminRepository()

    def register_student(self, db: Session, student: Student):
        existing_student = self.student_repository.find_by_email(
            db,
            student.email
        )

        if existing_student:
            raise ValueError("Student with this email already exists")

        return self.student_repository.create(db, student)

    def register_admin(self, db: Session, admin: Admin):
        existing_admin = self.admin_repository.find_by_email(
            db,
            admin.email
        )

        if existing_admin:
            raise ValueError("Admin with this email already exists")

        return self.admin_repository.create(db, admin)

    def login_student(
        self,
        db: Session,
        email: str,
        password: str
    ):
        student = self.student_repository.find_by_email(
            db,
            email
        )

        if student is None or student.password != password:
            raise ValueError("Invalid email or password")

        user = {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "department": student.department,
            "role": "student"
        }

        AuthState.login(user)

        return user

    def login_admin(
        self,
        db: Session,
        email: str,
        password: str
    ):
        admin = self.admin_repository.find_by_email(
            db,
            email
        )

        if admin is None or admin.password != password:
            raise ValueError("Invalid email or password")

        user = {
            "id": admin.id,
            "name": admin.name,
            "email": admin.email,
            "role": "admin"
        }

        AuthState.login(user)

        return user

    def logout(self):
        AuthState.logout()

        return {
            "message": "Logged out successfully"
        }