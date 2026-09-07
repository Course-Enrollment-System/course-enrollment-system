import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.course_model import CourseModel
from src.models.enrollment import CourseEnrollment
from src.models.student_model import StudentModel
from src.config.database import Base
from src.models.enrollment import CourseEnrollment
from src.models.semester import Semester
from src.repositories.enrollment_repository import EnrollmentRepository

# Create test engine
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@pytest.fixture(autouse=True)
def setup_db():
    # Force rebuild of tables with all registered models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

class TestEnrollmentRepository:

    def setup_method(self):
        Base.metadata.create_all(bind=engine)
        self.db = TestingSessionLocal()
        self.repository = EnrollmentRepository()

    def teardown_method(self):
        self.db.close()
        Base.metadata.drop_all(bind=engine)

    def test_create_enrollment(self):
        enrollment = CourseEnrollment(
            student_id=1,
            course_code="CSC101",
            session="2025/2026",
            semester=Semester.FIRST
            semester="First",
        )

        result = self.repository.create(self.db, enrollment)

        assert result["student_id"] == 1
        assert result["course_code"] == "CSC101"
        assert result["session"] == "2025/2026"
        assert result["semester"] == "FIRST"
        assert result["session"]=="2025/2026"
        assert result["semester"] == "First"
        assert result["id"] is not None

    def test_find_enrollment_by_id(self):
        enrollment = CourseEnrollment(
            student_id=1,
            course_code="CSC101",
            semester=Semester.FIRST,
            session="2025/2026"
            session="2025/2026",
            semester="First",
        )

        created = self.repository.create(self.db, enrollment)
        result = self.repository.find_by_id(self.db, created["id"])

        assert result["student_id"] == 1
        assert result["course_code"] == "CSC101"
        assert result["semester"] == "FIRST"
        assert result["session"] == "2025/2026"
        assert result["session"]=="2025/2026"
        assert result["semester"] == "First"

    def test_find_enrollment_by_id_not_found(self):
        result = self.repository.find_by_id(self.db, 999)
        assert result is None

    def test_find_all_enrollments(self):
        enrollment1 = CourseEnrollment(
            student_id=1,
            course_code="CSC101",
            semester=Semester.FIRST,
            session="2025/2026"
            session="2025/2026",
            semester="First",
        )
        enrollment2 = CourseEnrollment(
            student_id=1,
            course_code="MTH101",
            semester=Semester.FIRST,
            session="2025/2026"
            session="2025/2026",
            semester="First",
        )

        self.repository.create(self.db, enrollment1)
        self.repository.create(self.db, enrollment2)

        result = self.repository.find_all(self.db)
        assert len(result) == 2

    def test_find_all_enrollments_empty(self):
        result = self.repository.find_all(self.db)
        assert len(result) == 0

    def test_find_by_student_id(self):
        enrollment = CourseEnrollment(
            student_id=1,
            course_code="CSC101",
            semester=Semester.FIRST,
            session="2025/2026"
            session="2025/2026",

            semester="First",
        )

        self.repository.create(self.db, enrollment)
        result = self.repository.find_by_student_id(self.db, 1)

        assert len(result) == 1
        assert result[0]["student_id"] == 1
        assert result[0]["course_code"] == "CSC101"
        assert result[0]["semester"] == "FIRST"
        assert result[0]["session"] == "2025/2026"

    def test_find_by_student_id_not_found(self):
        result = self.repository.find_by_student_id(self.db, 999)
        assert len(result) == 0

    def test_create_multiple_enrollments(self):
        enrollment1 = CourseEnrollment(
            student_id=1,
            course_code="CSC101",
            semester=Semester.FIRST,
            session="2025/2026"
            session="2025/2026",

            semester="First",
        )
        enrollment2 = CourseEnrollment(
            student_id=1,
            course_code="MTH101",
            semester=Semester.FIRST,
            session="2025/2026"
            session="2025/2026",

            semester="First",
        )

        res1 = self.repository.create(self.db, enrollment1)
        res2 = self.repository.create(self.db, enrollment2)

        assert res1["id"] != res2["id"]

    def test_find_by_id_returns_semester(self):
        enrollment = CourseEnrollment(
            student_id=2,
            course_code="BUS111",
            semester=Semester.SECOND,
            session="2025/2026"
            session="2025/2026",

            semester="Second",
        )

        created = self.repository.create(self.db, enrollment)
        result = self.repository.find_by_id(self.db, created["id"])

        assert result["semester"] == "SECOND"

    def test_find_by_student_id_returns_multiple_enrollments(self):
        enrollment1 = CourseEnrollment(
            student_id=1,
            course_code="CSC101",
            semester=Semester.FIRST,
            session="2025/2026"
            session="2025/2026",

            semester="First",
        )
        enrollment2 = CourseEnrollment(
            student_id=1,
            course_code="MTH101",
            semester=Semester.FIRST,
            session="2025/2026"
            session="2025/2026",

            semester="First",
        )

        self.repository.create(self.db, enrollment1)
        self.repository.create(self.db, enrollment2)

        result = self.repository.find_by_student_id(self.db, 1)
        assert len(result) == 2