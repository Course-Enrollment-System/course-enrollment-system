from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.database import Base
from src.models.student import Student
from src.repositories.student_repository import StudentRepository


# as you can see i used SQLite for repository tests.
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


class TestStudentRepository:

    def setup_method(self):
        Base.metadata.create_all(bind=engine)

        self.db = TestingSessionLocal()
        self.repository = StudentRepository()

    def teardown_method(self):
        self.db.close()

        Base.metadata.drop_all(bind=engine)

    def test_create_student(self):
        student = Student(
            name="Azeez Azeez",
            email="az@example.com",
            department="Biochemistry",
            password="123456"
        )

        result = self.repository.create(self.db, student)


        assert result["name"] == "Azeez Azeez"
        assert result["email"] == "az@example.com"
        assert result["department"] == "Biochemistry"
        assert result["id"] is not None

    def test_find_student_by_id(self):
        student = Student(
            name="Azeez Azeez",
            email="az@example.com",
            department="Biochemistry",
            password="123456"
        )

        created = self.repository.create(self.db, student)

        result = self.repository.find_by_id(
            self.db,
            created["id"],
        )


        assert result["name"] == "Azeez Azeez"
        assert result["department"] == "Biochemistry"

    def test_find_student_by_id_not_found(self):
        result = self.repository.find_by_id(self.db, 999)

        assert result is None

    def test_find_all_students(self):
        student1 = Student(
            name="Azeez Azeez",
            email="az@example.com",
            department="Biochemistry",
            password="123456"
        )

        student2 = Student(
            name="Emeka Dike",
            email="dicks@example.com",
            department="Computer Science",
            password="654321"
        )

        self.repository.create(self.db, student1)
        self.repository.create(self.db, student2)

        result = self.repository.find_all(self.db)

        assert len(result) == 2

    def test_find_sstudent_by_email(self):
        student = Student(
            name="Azeez Azeez",
            email="az@example.com",
            department="Biochemistry",
            password="123456"
        )

        self.repository.create(self.db, student)

        result = self.repository.find_by_email(self.db,"az@example.com")

        assert result["name"] == "Azeez Azeez"
        assert result["email"] == "az@example.com"

    def test_find_by_email_not_found(self):
        result = self.repository.find_by_email(
            self.db,
            "missing@example.com",
        )

        assert result is None