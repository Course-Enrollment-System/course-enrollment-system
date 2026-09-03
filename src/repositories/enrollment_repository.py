from sqlalchemy.orm import Session

from src.models.enrollment import Enrollment
from src.models.enrollment_model import EnrollmentModel


class EnrollmentRepository:

    def create_enrollment(self, db: Session , enrollment: EnrollmentModel):
        return None




