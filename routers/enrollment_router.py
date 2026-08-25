from fastapi import APIRouter, Depends
from typing import List
from model.course_enrollment import Student, StudentCreate, Course, CourseCreate, EnrollmentCreate, CourseEnrolled
from services.enrollment_service import EnrollmentService

router = APIRouter()