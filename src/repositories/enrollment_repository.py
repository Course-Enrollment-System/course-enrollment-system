from sqlalchemy.orm import Session
from src.models.enrollment import CourseEnrollment
from src.models.enrollment_model import EnrollmentModel

class EnrollmentRepository:

    def create(self, db: Session, enrollment: CourseEnrollment):
        enrollment_model = EnrollmentModel(
            student_id=enrollment.student_id,
            course_code=enrollment.course_code,
            session=enrollment.session,
            semester=enrollment.semester
        )

        db.add(enrollment_model)
        db.commit()
        db.refresh(enrollment_model)

        semester_val = (
            enrollment_model.semester.value
            if hasattr(enrollment_model.semester, "value")
            else enrollment_model.semester
        )

        return {
            "id": enrollment_model.id,
            "student_id": enrollment_model.student_id,
            "course_code": enrollment_model.course_code,
            "session": enrollment_model.session,
            "semester": semester_val
        }

    def find_by_id(self, db: Session, enrollment_id: int):
        enrollment = (
            db.query(EnrollmentModel)
            .filter(EnrollmentModel.id == enrollment_id)
            .first()
        )

        if enrollment is None:
            return None

        semester_val = (
            enrollment.semester.value
            if hasattr(enrollment.semester, "value")
            else enrollment.semester
        )

        return {
            "id": enrollment.id,
            "student_id": enrollment.student_id,
            "course_code": enrollment.course_code,
            "session": enrollment.session,
            "semester": semester_val
        }

    def find_all(self, db: Session):
        enrollments = db.query(EnrollmentModel).all()

        return [
            {
                "id": enrollment.id,
                "student_id": enrollment.student_id,
                "course_code": enrollment.course_code,
                "session": enrollment.session,
                "semester": (
                    enrollment.semester.value
                    if hasattr(enrollment.semester, "value")
                    else enrollment.semester
                )
            }
            for enrollment in enrollments
        ]

    def find_by_student_id(self, db: Session, student_id: int):
        enrollments = (
            db.query(EnrollmentModel)
            .filter(EnrollmentModel.student_id == student_id)
            .all()
        )

        return [
            {
                "id": enrollment.id,
                "student_id": enrollment.student_id,
                "course_code": enrollment.course_code,
                "session": enrollment.session,
                "semester": (
                    enrollment.semester.value
                    if hasattr(enrollment.semester, "value")
                    else enrollment.semester
                )
            }
            for enrollment in enrollments
        ]