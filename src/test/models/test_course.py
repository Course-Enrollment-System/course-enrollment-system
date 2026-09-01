from pydantic import ValidationError
import pytest

from src.models.course import Course

class TestCourse:

    def test_create_course(self):
        course = Course(
            code="Bus111",
            title="Introduction to Business",
            credit_unit=4,
            department="Business Administration"

        )

        assert course.code == "Bus111"
        assert course.title == "Introduction to Business"
        assert course.credit_unit == 4

    def test_course_requires_code(self):
        with pytest.raises(ValidationError):
            Course(
                title="Introduction to Business",
                credit_unit=4,
                department="Business Administration"
            )

    def test_course_requires_title(self):
        with pytest.raises(ValidationError):
            Course(
                code="Bus111",
                credit_unit=4,
                department="Business Administration"
            )

    def test_course_requires_credit_unit(self):
        with pytest.raises(ValidationError):
            Course(
                code="Bus111",
                title="Introduction Business Administration",
                department="Business Administration"
            )

    def test_course_requires_department(self):
        with pytest.raises(ValidationError):
            Course(
                code="Bus111",
                title="Introduction to Business",
                credit_unit=4,
            )


