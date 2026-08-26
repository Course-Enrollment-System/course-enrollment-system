from bson import ObjectId

from src.config.database import students_collection
from src.models.student import Student


class StudentRepository:

    def create(self, student: Student):
        student_data = student.model_dump()

        result = students_collection.insert_one(student_data)

        return {
            "id": str(result.inserted_id),
            "name": student.name,
            "email": student.email,
            "department": student.department
        }

    def find_by_id(self, student_id: str):
        student = students_collection.find_one(
            {"_id": ObjectId(student_id)}
        )

        if student is None:
            return None

        return {
            "id": str(student["_id"]),
            "name": student["name"],
            "email": student["email"],
            "department": student["department"]
        }

    def find_all(self):
        students = students_collection.find()

        return [
            {
                "id": str(student["_id"]),
                "name": student["name"],
                "email": student["email"],
                "department": student["department"]
            }
            for student in students
        ]