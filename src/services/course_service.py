from sqlalchemy.orm import Session

from src.models.course import Course
from src.repositories.course_repository import CourseRepository


class CourseService:

    def __init__(self):
        self.course_repository = CourseRepository()

    def create_course(self, db: Session, course: Course):
        existing_course = self.course_repository.find_by_code(
            db,
            course.code
        )

        if existing_course:
            raise ValueError(
                "Course with this code already exists"
            )

        return self.course_repository.create(db, course)

    def find_by_code(self, db: Session, code: str):
        course = self.course_repository.find_by_code(
            db,
            code
        )

        if course is None:
            raise ValueError(
                "Course with this code does not exist"
            )

        return course

    def find_all(self, db: Session):
        return self.course_repository.find_all(db)