from sqlalchemy.orm import Session

from src.models.course import Course
from src.repositories.course_repository import CourseRepository
from src.services.auth_state import AuthState


class CourseService:

    def __init__(self):
        self.course_repository = CourseRepository()

    def create_course(self, db: Session, course: Course):

        current_user = AuthState.get_current_user()

        # this will check if the admin is logged in
        if current_user is None:
            raise PermissionError("You're not logged in")

        # this is to check if  is logged in, but isn't an admin
        if current_user["role"] != "admin":
            raise PermissionError("Only admins can create courses")

        # Check if course already exists
        existing_course = self.course_repository.find_by_code(
            db,
            course.code
        )

        if existing_course:
            raise ValueError(
                "Course with this code already exists"
            )

        return self.course_repository.create(
            db,
            course
        )

    def find_by_code(self, db: Session, code: str):

        course = self.course_repository.find_by_code(db,code)

        if course is None:
            raise ValueError(
                "Course with this code does not exist"
            )

        return course

    def find_all(self, db: Session):
        return self.course_repository.find_all(db)


    def delete_by_curse_code(self, db: Session, code: str):
        current_user = AuthState.get_current_user()

        if current_user is None:
            raise PermissionError("You're not logged in")

        if current_user["role"] != "admin":
            raise PermissionError("Only admin can delete courses")

        existing_course = self.course_repository.find_by_code(db,code)

        if existing_course is None:
            raise ValueError("course doesn't exist")

        return self.course_repository.delete_by_code(db,code)