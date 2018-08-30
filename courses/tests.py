from django_dynamic_fixture import G

from courses.models import Student, Course
from test_services.lp_test_case import LPTestCase


class CoursesTestCase(LPTestCase):
    def test_cards_works_only_with_logged_user(self):
        course1: Course = G(Course)
        student1: Student = G(Student, course=course1)

        course2: Course = G(Course)
        course3: Course = G(Course, teacher=student1.user)
        courses = Course.get_user_courses(student1.user)
        self.assertEqual(len(courses), 2)
        for course in courses:
            self.assertIn(course.id, [course1.id, course3.id])
