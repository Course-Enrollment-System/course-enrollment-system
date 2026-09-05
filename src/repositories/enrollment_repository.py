from sqlalchemy.orm import Session

from src.models.enrollment import Enrollment
from src.models.enrollment_model import EnrollmentModel


class EnrollmentRepository:

    def create(self, db: Session , enrollment: EnrollmentModel):

                enrollment_model = EnrollmentModel(
                    student_id=enrollment.student_id,
                    course_code=enrollment.course_code,
                    semester=enrollment.semester
                )

                db.add(enrollment_model)
                db.commit()
                db.refresh(enrollment_model)

                return {
                    "id": enrollment_model.id,
                    "student_id": enrollment_model.student_id,
                    "course_code": enrollment_model.course_code,
                    "semester": enrollment_model.semester
                }

    def find_by_id(self, db: Session, enrollment_id: int):
                enrollment = (
                    db.query(EnrollmentModel)
                    .filter(EnrollmentModel.id == enrollment_id)
                    .first()
                )

                if enrollment is None:
                    return None

                return {
                    "id": enrollment.id,
                    "student_id": enrollment.student_id,
                    "course_code": enrollment.course_code,
                    "semester": enrollment.semester
                }

    def find_all(self, db: Session):
                enrollments = db.query(EnrollmentModel).all()

                return [
                    {
                        "id": enrollment.id,
                        "student_id": enrollment.student_id,
                        "course_code": enrollment.course_code,
                        "semester": enrollment.semester
                    }
                    for enrollment in enrollments
                ]

    def find_by_student_id(self, db: Session, student_id: int):
                return (
                    db.query(EnrollmentModel)
                    .filter(EnrollmentModel.student_id == student_id)
                    .all()
                )




