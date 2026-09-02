from unittest.mock import Mock

import pytest

from src.models.course import Course
from src.services.course_service import CourseService


class TestCourseService:

    def test_create_course_with_existing_code(self):
        repository = Mock()
        db = Mock()

        repository.find_by_code.return_value = {
            "id": 1,
            "code": "CSC101",
            "title": "Introduction to Computer Science",
            "credit_unit": 3,
            "department": "Computer Science",
        }

        service = CourseService()
        service.course_repository = repository

        course = Course(
            code="CSC101",
            title="Introduction to Computer Science",
            credit_unit=3,
            department="Computer Science",
        )

        with pytest.raises(
            ValueError,
            match="Course with this code already exists",
        ):
            service.create_course(db, course)

        repository.create.assert_not_called()

    def test_create_course(self):
        repository = Mock()
        db = Mock()

        repository.find_by_code.return_value = None

        repository.create.return_value = {
            "id": 1,
            "code": "CSC101",
            "title": "Introduction to Computer Science",
            "credit_unit": 3,
            "department": "Computer Science",
        }

        service = CourseService()
        service.course_repository = repository

        course = Course(
            code="CSC101",
            title="Introduction to Computer Science",
            credit_unit=3,
            department="Computer Science",
        )

        result = service.create_course(db, course)

        assert result["code"] == "CSC101"
        assert result["title"] == "Introduction to Computer Science"
        assert result["credit_unit"] == 3
        assert result["department"] == "Computer Science"

        repository.find_by_code.assert_called_once_with(db,course.code,)

        repository.create.assert_called_once_with(db,course,)

    def test_get_course_by_code(self):
        repository = Mock()
        db = Mock()

        repository.find_by_code.return_value = {
            "id": 1,
            "code": "CSC101",
            "title": "Introduction to Computer Science",
            "credit_unit": 3,
            "department": "Computer Science",
        }

        service = CourseService()
        service.course_repository = repository

        result = service.find_by_code(db, "CSC101")

        assert result["title"] == "Introduction to Computer Science"

    def test_get_course_by_code_not_found(self):
        repository = Mock()
        db = Mock()

        repository.find_by_code.return_value = None

        service = CourseService()
        service.course_repository = repository

        with pytest.raises(
            ValueError,match= "Course with this code does not exist"
        ):
            service.find_by_code(db, "CSC101")

        repository.create.assert_not_called()

    def test_get_all_courses(self):
        repository = Mock()
        db = Mock()

        repository.find_all.return_value = [
            {
            "id": 1,
            "code": "CSC101",
            "title": "Introduction to Computer Science",
            "credit_unit": 3,
            "department": "Computer Science",
        },

        {
            "id": 2,
            "code": "CSC201",
            "title": "Introduction to Programming",
            "credit_unit": 6,
            "department": "Computer Science",

        },
        ]

        service = CourseService()
        service.course_repository = repository

        result = service.find_all(db)
        assert len(result) == 2

        repository.find_all.assert_called_once_with(db)


