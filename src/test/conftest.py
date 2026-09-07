import os

from test.test_db_setup import Base, engine
from src.models.enrollment import CourseEnrollment


# please use SQLite instead of the MySQL database for test.
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

# conftest.py or test setup
  # Ensure model is imported FIRST





# In your pytest test setup/conftest.py
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)



import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.database import Base
from src.models.course_model import CourseModel
from src.models.enrollment import CourseEnrollment
from src.models.student_model import StudentModel

engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)