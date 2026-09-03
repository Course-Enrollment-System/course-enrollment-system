from sqlalchemy.orm import Session

from src.models.course import Course
from src.models.course_model import CourseModel


class CourseRepository:

    def create(self, db: Session, course: Course):
        course_model = CourseModel(
            code=course.code,
            title=course.title,
            credit_unit=course.credit_unit,
            department=course.department
        )

        db.add(course_model)
        db.commit()
        db.refresh(course_model)

        return {
            "id": course_model.id,
            "code": course_model.code,
            "title": course_model.title,
            "credit_unit": course_model.credit_unit,
            "department": course_model.department
        }

#finding course by its code is way better, this is just a duplicate that's why i comment this out

    def find_by_id(self, db: Session, course_id: int):
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()

        if course is None:
            return None

        return {
            "id": course.id,
            "code": course.code,
            "title": course.title,
            "credit_unit": course.credit_unit,
            "department": course.department
        }

    def find_all(self, db: Session):
        courses = db.query(CourseModel).all()

        return [
            {
                "id": course.id,
                "code": course.code,
                "title": course.title,
                "credit_unit": course.credit_unit,
                "department": course.department
            }
            for course in courses
        ]

    def find_by_code(self, db: Session, code: str):
        print("sdfg 1d")
        course = db.query(CourseModel).filter(CourseModel.code == code).first()

        if course is None:
            return None
        print("dfdddfggedfg")
        return {
            "id": course.id,
            "code": course.code,
            "title": course.title,
            "credit_unit": course.credit_unit,
            "department": course.department
        }

    def delete_by_code(self, db: Session, code: str):
        course = db.query(CourseModel).filter(CourseModel.code == code).first()

        if course is None:
            return None

        db.delete(course)
        db.commit()

        return {
            "code": course.code,
            "title": course.title,
        }