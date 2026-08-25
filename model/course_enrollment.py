from pydantic import BaseModel


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department: str



class Student(StudentCreate):
    id: int



class CourseCreate(BaseModel):
    code: str
    title: str
    department: str


class Course(CourseCreate):
    id: int



class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class CourseEnrolled(EnrollmentCreate):
    id: int

