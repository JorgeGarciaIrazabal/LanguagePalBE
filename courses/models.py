from datetime import datetime

from ajson import AJson
from django.db import models
from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from lp_auth.models import User


@AJson()
class Course(models.Model):
    id: int
    ''' @aj(groups='["course_basic","course_detailed"]') '''
    teacher: User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ''' @aj(groups='["course_basic","course_detailed"]') '''
    title: str = models.CharField(max_length=150)
    ''' @aj(groups='["course_basic","course_detailed"]' required) '''
    description: str = models.CharField(max_length=500, null=True)
    ''' @aj(groups='["course_basic","course_detailed"]') '''

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    ''' @aj(groups='["course_detailed"]') '''
    updated_at: datetime = models.DateTimeField(auto_now=True)
    ''' @aj(groups='["course_detailed"]') '''

    @staticmethod
    def get_user_courses(user: User):
        return Course.objects.filter(Q(teacher=user) | Q(student__user=user))

    @staticmethod
    def get_or_404(pk: int, user: User):
        return get_object_or_404(Course, (Q(teacher=user) | Q(student__user=user)) & Q(pk=pk))


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


@AJson()
class Card(models.Model):
    id: int
    ''' @aj(groups='["card_basic","card_detailed"]') '''
    text: str = models.CharField(max_length=300, unique=True)
    ''' @aj(groups='["card_basic","card_detailed"]' required) '''
    sentence: str = models.CharField(max_length=1000, null=True)
    ''' @aj(groups='["card_basic","card_detailed"]') '''
    definition: str = models.CharField(max_length=1000, null=True)
    ''' @aj(groups='["card_basic","card_detailed"]') '''
    translation: str = models.CharField(max_length=1000)
    ''' @aj(groups='["card_basic","card_detailed"]') required'''
    sound_path: str = models.CharField(max_length=300, null=True)
    ''' @aj(groups='["card_basic","card_detailed"]') '''
    sentence_sound_path: str = models.CharField(max_length=300, null=True)
    ''' @aj(groups='["card_basic","card_detailed"]') '''
    creator: User = models.ForeignKey(User, on_delete=models.CASCADE)
    ''' @aj(groups='["card_detailed"]') '''
    course: Course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    ''' @aj(groups='["card_detailed"]') '''
    updated_at: datetime = models.DateTimeField(auto_now=True)
    ''' @aj(groups='["card_detailed"]') '''

    @staticmethod
    def get_user_cards(user: User) -> QuerySet:
        return Card.objects.filter(creator=user)


# used to validate data to update
class UpdateCard(Card):
    id: int  # @aj(groups='[]')
    created_at: datetime  # @aj(groups='[]')
    updated_at: datetime  # @aj(groups='[]')
    creator: User  # @aj(groups='[]')
    course_id: int  # @aj(groups='["card_basic"]' required)

    class Meta:
        managed = False
