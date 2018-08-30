from datetime import datetime, timedelta
from typing import Tuple

import jwt
from ajson import ASerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request

from language_pal_be import settings
from lp_auth.models import User
from lp_auth.permissions import IsAnonymous
from lp_auth.types import LoginBody


@api_view(['post'])
@permission_classes([IsAnonymous])
def login(request: Request):
    login_body: LoginBody = ASerializer().from_dict(request.data, LoginBody)
    try:
        jwt_token, user = login_from_params(login_body.email, login_body.password)
        return JsonResponse(
            ASerializer().to_dict({'token': jwt_token, 'user': user}, groups=['user_detailed']),
            status=200,
        )
    except User.DoesNotExist:
        return JsonResponse({'Error': "Invalid username/password"}, status="400")


@api_view(['post'])
@permission_classes([IsAnonymous])
def signup(request):
    user: User = ASerializer().from_dict(request.data, User)
    user.save()
    jwt_token = __construct_token(user)
    return JsonResponse(
        ASerializer().to_dict({'token': jwt_token, 'user': user}, groups=['user_detailed']),
        status=200,
    )


def __construct_token(user: User) -> str:
    payload = {
        'expires_in': datetime.utcnow() + timedelta(days=365),
        'user_id': user.id,
    }
    return jwt.encode(ASerializer().to_dict(payload), settings.JWT_SECRET_KEY).decode('utf-8')


def login_from_params(email: str, password: str) -> Tuple[str, User]:
    user = User.objects.get(email=email, password=password)
    jwt_token = __construct_token(user)
    return jwt_token, user
