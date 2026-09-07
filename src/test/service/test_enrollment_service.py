import pytest
from src.models.course_model import CourseModel
from src.models.enrollment import CourseEnrollment
from src.models.semester import Semester
from src.services.auth_state import AuthState
from src.services.enrollment_services import EnrollmentService
from src.test.test_db_setup import db_session

# Standard helper functions to simulate user states
def get_no_user():
    return None

def get_admin_user():
    return {"id": 1, "role": "admin"}

def get_student_user():
    return {"id": 1, "role": "student"}


class TestEnrollmentService:

    def setup_method(self):
        self.service = EnrollmentService()
        self.sample_enrollment = CourseEnrollment(
            student_id=1,
            course_code="CSC101",
            session="2025/2026",
            semester=Semester.FIRST
        )

    # 1. User not logged in
    def test_register_when_not_logged_in(self, db_session):
        AuthState.get_current_user = get_no_user

        with pytest.raises(ValueError, match="You are not logged in"):
            self.service.register_course(db_session, self.sample_enrollment)

    # 2. User is not a student
    def test_register_when_not_a_student(self, db_session):
        AuthState.get_current_user = get_admin_user

        with pytest.raises(ValueError, match="Only students can register courses"):
            self.service.register_course(db_session, self.sample_enrollment)

    # 3. Course does not exist in DB
    def test_register_course_not_found(self, db_session):
        AuthState.get_current_user = get_student_user

        with pytest.raises(ValueError, match="Course with code CSC101 does not exist"):
            self.service.register_course(db_session, self.sample_enrollment)

        # 4. Successful Registration
        def test_register_course_success(self, db_session):
            AuthState.get_current_user = get_student_user
            course = CourseModel(
                code="CSC101",
                title="Intro to CS",
                credit_unit=3,
                department="Computer Science"
            )
            db_session.add(course)
            db_session.commit()

            # Call service once (returns an ORM object or schema)
            result = self.service.register_course(db_session, self.sample_enrollment)

            # Assert directly on the returned result object
            assert result.id is not None
            assert result.course_code == "CSC101"

        # 5. Get Student Enrollments
        def test_get_student_enrollments(self, db_session):
            AuthState.get_current_user = get_student_user

            course = CourseModel(
                code="CSC101",
                title="Intro to CS",
                credit_unit=3,
                department="Computer Science"
            )
            db_session.add(course)
            db_session.commit()
            self.service.register_course(db_session, self.sample_enrollment)
            result = self.service.get_student_enrollments(db_session, student_id=1)
            assert len(result) == 1
            assert result[0].course_code == "CSC101"