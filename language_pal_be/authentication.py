from datetime import datetime

import jwt
from ajson import ASerializer
from django.conf import settings
from rest_framework import authentication

from lp_auth.models import User
from lp_auth.types import DecodedToken


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        authorization = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', "", 1)
        if authorization == '':
            return None
        decoded_token = jwt.decode(authorization, settings.JWT_SECRET_KEY)
        token: DecodedToken = ASerializer().from_dict(decoded_token, DecodedToken)
        if token.expires_in <= datetime.utcnow():
            raise jwt.exceptions.ExpiredSignatureError()
        user = User.objects.get(id=token.user_id)
        if user is None:
            raise jwt.exceptions.ImmatureSignatureError()
        return user, token

    def authenticate_header(self, request):
        return 'Bearer token_type="JWT"'
