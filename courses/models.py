from datetime import datetime

from ajson import AJson
from django.db import models
from django.db.models import Q

from lp_auth.models import User


@AJson()
class Course(models.Model):
    id: int
    ''' @aj(groups='["course_basic","course_detailed"]') '''
    teacher: User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ''' @aj(groups='["course_basic","course_detailed"]') '''
    title: str = models.CharField(max_length=150)
    ''' @aj(groups='["course_basic","course_detailed"]' required) '''

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    ''' @aj(groups='["course_detailed"]') '''
    updated_at: datetime = models.DateTimeField(auto_now=True)
    ''' @aj(groups='["course_detailed"]') '''

    @staticmethod
    def get_user_courses(user):
        return Course.objects.filter(Q(teacher=user) | Q(student__user=user))


@AJson()
class Student(models.Model):
    id: int
    ''' @aj(groups='["student_basic","student_detailed"]') '''
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    ''' @aj(groups='["student_basic","student_detailed"]') '''
    course: Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ''' @aj(groups='["student_detailed"]') '''

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    ''' @aj(groups='["student_detailed"]') '''
    updated_at: datetime = models.DateTimeField(auto_now=True)
    ''' @aj(groups='["student_detailed"]') '''

    class Meta:
        unique_together = ('user', 'course',)
