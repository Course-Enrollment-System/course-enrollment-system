from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.database import Base
from src.models.course import Course
from src.repositories.course_repository import CourseRepository


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


class TestCourseRepository:

    def setup_method(self):
        Base.metadata.create_all(bind=engine)

        self.db = TestingSessionLocal()
        self.repository = CourseRepository()

    def teardown_method(self):
        self.db.close()

        Base.metadata.drop_all(bind=engine)

    def test_create_course(self):
        course = Course(
            code="CSC101",
            title="Introduction to Computer Science",
            credit_unit=3,
            department="Computer Science",
        )

        result = self.repository.create(self.db, course)

        assert result["code"] == "CSC101"
        assert result["title"] == "Introduction to Computer Science"
        assert result["credit_unit"] == 3
        assert result["department"] == "Computer Science"
        assert result["id"] is not None

    def test_find_course_by_id(self):
        course = Course(
            code="CSC101",
            title="Introduction to Computer Science",
            credit_unit=3,
            department="Computer Science",
        )

        created = self.repository.create(self.db, course)

        result = self.repository.find_by_id(
            self.db,
            created["id"],
        )

        assert result["code"] == "CSC101"
        assert result["department"] == "Computer Science"

    def test_find_course_by_id_not_found(self):
        result = self.repository.find_by_id(self.db, 999)

        assert result is None

    def test_find_all_courses(self):
        course1 = Course(
            code="CSC101",
            title="Introduction to Computer Science",
            credit_unit=3,
            department="Computer Science",
        )

        course2 = Course(
            code="MTH101",
            title="General Mathematics",
            credit_unit=3,
            department="Mathematics",
        )

        self.repository.create(self.db, course1)
        self.repository.create(self.db, course2)

        result = self.repository.find_all(self.db)

        assert len(result) == 2

    def test_find_all_courses_empty(self):
        result = self.repository.find_all(self.db)

        assert len(result) == 0

    def test_find_by_code(self):
        course = Course(
            code="CSC101",
            title="Introduction to Computer Science",
            credit_unit=3,
            department="Computer Science",
        )

        self.repository.create(self.db, course)

        result = self.repository.find_by_code(
            self.db,
            "CSC101",
        )

        assert result["code"] == "CSC101"
        assert result["title"] == "Introduction to Computer Science"

    def test_find_by_code_not_found(self):
        result = self.repository.find_by_code(
            self.db,
            "NOTEXIST",
        )

        assert result is None

    def test_create_multiple_courses(self):
        course1 = Course(
            code="CSC101",
            title="Introduction to Computer Science",
            credit_unit=3,
            department="Computer Science",
        )

        course2 = Course(
            code="MTH101",
            title="General Mathematics",
            credit_unit=3,
            department="Mathematics",
        )

        res1 = self.repository.create(self.db, course1)
        res2 = self.repository.create(self.db, course2)

        assert res1["id"] != res2["id"]

    def test_find_by_id_returns_credit_unit(self):
        course = Course(
            code="BCH201",
            title="General Biochemistry",
            credit_unit=4,
            department="Biochemistry",
        )

        created = self.repository.create(self.db, course)

        result = self.repository.find_by_id(
            self.db,
            created["id"],
        )

        assert result["credit_unit"] == 4

    def test_find_by_code_returns_department(self):
        course = Course(
            code="PHY101",
            title="General Physics",
            credit_unit=3,
            department="Physics",
        )

        self.repository.create(self.db, course)

        result = self.repository.find_by_code(
            self.db,
            "PHY101",
        )

        assert result["department"] == "Physics"