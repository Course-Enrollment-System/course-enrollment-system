from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.database import Base
from src.models.enrollment import Enrollment
from src.repositories.enrollment_repository import EnrollmentRepository


DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class TestEnrollmentRepository:

    def setup_method(self):
        Base.metadata.create_all(bind=engine)

        self.db = TestingSessionLocal()
        self.repository = EnrollmentRepository()

    def teardown_method(self):
        self.db.close()

        Base.metadata.drop_all(bind=engine)

    def test_create_enrollment(self):
        enrollment = Enrollment(
            student_id=1,
            course_code="CSC101",
            session="2025/2026",
            semester="First",
        )

        result = self.repository.create(
            self.db,
            enrollment,
        )

        assert result["student_id"] == 1
        assert result["course_code"] == "CSC101"
        assert result["session"]=="2025/2026"
        assert result["semester"] == "First"
        assert result["id"] is not None

    def test_find_enrollment_by_id(self):
        enrollment = Enrollment(
            student_id=1,
            course_code="CSC101",
            session="2025/2026",
            semester="First",
        )

        created = self.repository.create(
            self.db,
            enrollment,
        )

        result = self.repository.find_by_id(
            self.db,
            created["id"],
        )

        assert result["student_id"] == 1
        assert result["course_code"] == "CSC101"
        assert result["session"]=="2025/2026"
        assert result["semester"] == "First"

    def test_find_enrollment_by_id_not_found(self):
        result = self.repository.find_by_id(
            self.db,
            999,
        )

        assert result is None

    def test_find_all_enrollments(self):
        enrollment1 = Enrollment(
            student_id=1,
            course_code="CSC101",
            session="2025/2026",
            semester="First",
        )

        enrollment2 = Enrollment(
            student_id=1,
            course_code="MTH101",
            session="2025/2026",
            semester="First",
        )

        self.repository.create(
            self.db,
            enrollment1,
        )

        self.repository.create(
            self.db,
            enrollment2,
        )

        result = self.repository.find_all(self.db)

        assert len(result) == 2

    def test_find_all_enrollments_empty(self):
        result = self.repository.find_all(self.db)

        assert len(result) == 0

    def test_find_by_student_id(self):
        enrollment = Enrollment(
            student_id=1,
            course_code="CSC101",
            session="2025/2026",

            semester="First",
        )

        self.repository.create(
            self.db,
            enrollment,
        )

        result = self.repository.find_by_student_id(
            self.db,
            1,
        )

        assert len(result) == 1
        assert result[0].student_id == 1
        assert result[0].course_code == "CSC101"

    def test_find_by_student_id_not_found(self):
        result = self.repository.find_by_student_id(
            self.db,
            999,
        )

        assert len(result) == 0

    def test_create_multiple_enrollments(self):
        enrollment1 = Enrollment(
            student_id=1,
            course_code="CSC101",
            session="2025/2026",

            semester="First",
        )

        enrollment2 = Enrollment(
            student_id=1,
            course_code="MTH101",
            session="2025/2026",

            semester="First",
        )

        res1 = self.repository.create(
            self.db,
            enrollment1,
        )

        res2 = self.repository.create(
            self.db,
            enrollment2,
        )

        assert res1["id"] != res2["id"]

    def test_find_by_id_returns_semester(self):
        enrollment = Enrollment(
            student_id=2,
            course_code="BUS111",
            session="2025/2026",

            semester="Second",
        )

        created = self.repository.create(
            self.db,
            enrollment,
        )

        result = self.repository.find_by_id(
            self.db,
            created["id"],
        )

        assert result["semester"] == "Second"

    def test_find_by_student_id_returns_multiple_enrollments(self):
        enrollment1 = Enrollment(
            student_id=1,
            course_code="CSC101",
            session="2025/2026",

            semester="First",
        )

        enrollment2 = Enrollment(
            student_id=1,
            course_code="MTH101",
            session="2025/2026",

            semester="First",
        )

        self.repository.create(
            self.db,
            enrollment1,
        )

        self.repository.create(
            self.db,
            enrollment2,
        )

        result = self.repository.find_by_student_id(
            self.db,
            1,
        )

        assert len(result) == 2