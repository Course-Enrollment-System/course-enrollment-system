from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.database import Base
from src.models.admin import Admin
from src.repositories.admin_repository import AdminRepository


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

class TestAdminRepository:

    def setup_method(self):
        Base.metadata.create_all(bind=engine)

        self.db = TestingSessionLocal()
        self.repository = AdminRepository()

    def teardown_method(self):
        self.db.close()

        Base.metadata.drop_all(bind=engine)




    def test_create_admin(self):
        repository = AdminRepository()

        admin = Admin(
            name="Admin",
            email="admin@yahoo.com",
            password="123456"
        )

        result = self.repository.create(self.db, admin)

        assert result["name"] == "Admin"


    def test_find_admin_by_email(self):
        repository = AdminRepository()

        admin = Admin(
            name="Admin",
            email="admin2@yahoo.com",
            password="123456"
        )

        repository.create(self.db, admin)

        result = repository.find_by_email(self.db, "admin2@yahoo.com")

        assert result is not None
        assert result.email == "admin2@example.com"
        assert result.password == "123456"