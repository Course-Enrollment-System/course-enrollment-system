from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.database import Base
from src.models.student_model import StudentModel
from src.repositories.student_repository import StudentRepository# Ensure your model is imported

# 1. Create a temporary in-memory database JUST for testing
test_engine = create_engine("sqlite:///:memory:")
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


class TestStudentRepository:
    def setup_method(self):
        # 2. Build fresh tables in RAM (completely ignores your local .db file)
        Base.metadata.create_all(bind=test_engine)

        # 3. Bind your test session to the memory database
        self.db = TestSessionLocal()
        self.repository = StudentRepository()

    def teardown_method(self):
        # 4. Clean up the RAM database after each test
        self.db.close()
        Base.metadata.drop_all(bind=test_engine)

    def test_create_student(self):
        student = StudentModel(
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
        student = StudentModel(
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
        student1 = StudentModel(
            name="Azeez Azeez",
            email="az@example.com",
            department="Biochemistry",
            password="123456"
        )

        student2 = StudentModel(
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
        student = StudentModel(
            name="Azeez Azeez",
            email="az@example.com",
            department="Biochemistry",
            password="123456"
        )

        print(student.name)

        self.repository.create(self.db, student)

        result = self.repository.find_by_email(self.db,"az@example.com")

        assert result.department == "Biochemistry"


    def test_find_by_email_not_found(self):
        result = self.repository.find_by_email(
            self.db,
            "missing@example.com",
        )

        assert result is None