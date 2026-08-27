from src.config.database import Base, engine
from src.models.student_model import StudentModel


# Create database tables.
# In normal use, this creates the tables in MySQL.
Base.metadata.create_all(bind=engine)