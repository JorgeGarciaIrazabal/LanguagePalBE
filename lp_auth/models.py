from datetime import datetime

from ajson import AJson
from django.db import models


@AJson()
class User(models.Model):
    id: int
    ''' @aj(groups='["user_basic","user_detailed"]') '''

    first_name: str = models.CharField(max_length=30, null=True)
    ''' @aj(groups='["user_basic","user_detailed"]') '''
    last_name: str = models.CharField(max_length=150, null=True)
    ''' @aj(groups='["user_basic","user_detailed"]') '''
    email: str = models.EmailField(blank=False, unique=True)
    ''' @aj(groups='["user_basic","user_detailed"]') '''
    photo_path: str = models.CharField(max_length=300, null=True)
    ''' @aj(groups='["user_basic","user_detailed"]') '''
    is_admin = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    ''' @aj(groups='["user_detailed"]') '''

    password: str = models.CharField(max_length=150)
    ''' @aj(groups='[]') '''

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    ''' @aj(groups='["user_detailed"]') '''
    updated_at: datetime = models.DateTimeField(auto_now=True)
    ''' @aj(groups='["user_detailed"]') '''
