from datetime import datetime

from ajson import AJson
from django.db import models
from django.db.models import QuerySet

from courses.models import Course
from lp_auth.models import User


@AJson()
class Card(models.Model):
    id: int
    ''' @aj(groups='["card_basic","card_detailed"]') '''
    text: str = models.CharField(max_length=300, unique=True)
    ''' @aj(groups='["card_basic","card_detailed"]' required) '''
    sentence: str = models.CharField(max_length=1000, null=True)
    ''' @aj(groups='["card_basic","card_detailed"]') '''
    sound_path: str = models.CharField(max_length=300, null=True)
    ''' @aj(groups='["card_detailed"]') '''
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    ''' @aj(groups='["card_detailed"]') '''
    course: Course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    ''' @aj(groups='["card_detailed"]') '''
    updated_at: datetime = models.DateTimeField(auto_now=True)
    ''' @aj(groups='["card_detailed"]') '''

    @staticmethod
    def get_user_cards(user: User) -> QuerySet:
        return Card.objects.filter(user=user)


# used to validate data to update
class UpdateCard(Card):
    id: int  # @aj(groups='[]')
    created_at: datetime  # @aj(groups='[]')
    updated_at: datetime  # @aj(groups='[]')
    user: User  # @aj(groups='[]')

    class Meta:
        managed = False
