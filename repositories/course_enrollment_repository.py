from abc import ABC, abstractmethod
from typing import List, Optional
from model.course_enrollment import Student, StudentCreate, Course, CourseCreate, EnrollmentCreate, CourseEnrolled

class CourseEnrollmentRepository(ABC):

    @abstractmethod
    def create_student(self, student: StudentCreate) -> Student:
        pass

    @abstractmethod
    def get_all_students(self) -> List[Student]:
        pass

    @abstractmethod
    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        pass

    @abstractmethod
    def create_course(self, course: CourseCreate) -> Course:
        pass

    @abstractmethod
    def get_all_courses(self) -> List[Course]:
        pass

    @abstractmethod
    def get_course_by_id(self, course_id: int) -> Optional[Course]:
        pass

    @abstractmethod
    def create_enrollment(self, enrollment: EnrollmentCreate) -> CourseEnrolled:
        pass

    @abstractmethod
    def get_all_enrollments(self) -> List[CourseEnrolled]:
        pass

    