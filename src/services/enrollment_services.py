from sqlalchemy.orm import Session
from src.models.enrollment import CourseEnrollment
from src.repositories.enrollment_repository import EnrollmentRepository
from src.repositories.course_repository import CourseRepository
from src.services.auth_state import AuthState

class EnrollmentService:

    def __init__(self):
        self.enrollment_repository = EnrollmentRepository()
        self.course_repository = CourseRepository()

    def register_course(self, db: Session, enrollment: CourseEnrollment):
        current_user = AuthState.get_current_user()

        if current_user is None:
            raise ValueError("You are not logged in")

        if current_user["role"] != "student":
            raise ValueError("Only students can register courses")

        # Ensure single course exists
        course = self.course_repository.find_by_code(db, enrollment.course_code)
        if course is None:
            raise ValueError(f"Course with code {enrollment.course_code} does not exist")

        return self.enrollment_repository.create(db, enrollment)

    def get_student_enrollments(self, db: Session, student_id: int):
        return self.enrollment_repository.find_by_student_id(db, student_id)