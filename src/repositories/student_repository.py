from sqlalchemy.orm import Session

from models.student import Student
from src.models.student_model import StudentModel


class StudentRepository:

    def create(self, db: Session, student: Student):
        student_model = StudentModel(
            name=student.name,
            email=student.email,
            department=student.department,
            password=student.password
        )

        db.add(student_model)
        db.commit()
        db.refresh(student_model)

        return {
            "id": student_model.id,
            "name": student_model.name,
            "email": student_model.email,
            "department": student_model.department
        }

    def find_by_id(self, db: Session, student_id: int):
        student = db.query(StudentModel).filter(
            StudentModel.id == student_id
        ).first()

        if student is None:
            return None

        return {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "department": student.department
        }

    def find_all(self, db: Session):
        students = db.query(StudentModel).all()

        return [
            {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "department": student.department
            }
            for student in students
        ]

    def find_by_email(self, db: Session, email: str):
        if email is None:
            return None

        return db.query(StudentModel).filter(StudentModel.email == email).first()