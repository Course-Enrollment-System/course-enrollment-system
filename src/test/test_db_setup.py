from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


# 1. Define Student FIRST
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)


# 2. Define Enrollment SECOND (referencing students.id)
class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))


# 3. Connect to SQLite (creates a local file named test.db)
engine = create_engine("sqlite:///test.db")

# 4. Create the tables
Base.metadata.create_all(engine)

# 5. Use it
Session = sessionmaker(bind=engine)
db = Session()

# Insert data
new_student = Student(name="Alex")
db.add(new_student)
db.commit()

new_enrollment = Enrollment(student_id=new_student.id)
db.add(new_enrollment)
db.commit()

print("Done! Database created and working.")


def db_session():
    return None