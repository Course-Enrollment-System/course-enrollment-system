from src.config.database import Base, engine


from src.models.student_model import StudentModel
from src.models.course_model import CourseModel
from src.models.admin_model import AdminModel

# this makes SQLAlchemy knows the  models tables.

def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()