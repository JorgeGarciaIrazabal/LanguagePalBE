from typing import Type, Optional

from ajson import ASerializer
from django.urls import NoReverseMatch, reverse
from test_plus.test import TestCase as PlusTestCase

from lp_auth.models import User
from lp_auth.views import login_from_params


class LPTestCase(PlusTestCase):
    current_token: str

    def setUp(self):
        super().setUp()
        self.current_token = None

    def request_json(self, method_name, url: str, body: dict = None, *args, **kwargs):
        valid_method_names = [
            'get',
            'post',
            'put',
            'patch',
        ]

        if method_name in valid_method_names:
            method = getattr(self.client, method_name)
        else:
            raise LookupError("Cannot find the method {0}".format(method_name))
        try:
            final_url = reverse(url, args=args, kwargs=kwargs)
        except NoReverseMatch:
            final_url = url

        if self.current_token is not None:
            kwargs['HTTP_AUTHORIZATION'] = 'Bearer ' + self.current_token
        self.last_response = method(
            final_url,
            None if method_name == 'get' else ASerializer().serialize(body),
            content_type="application/json",
            *args,
            **kwargs
        )
        self.context = self.last_response.context
        return self.last_response

    def post_json(self, url: str, body: dict, *args, **kwargs):
        return self.request_json('post', url, body, *args, **kwargs)

    def put_json(self, url: str, body: dict, *args, **kwargs):
        return self.request_json('put', url, body, *args, **kwargs)

    def patch_json(self, url: str, body: dict, *args, **kwargs):
        return self.request_json('patch', url, body, *args, **kwargs)

    def get_content_json(self, response=None, _class: Optional[Type] = None):
        if response is None:
            response = self.last_response
        return ASerializer().unserialize(response.content, _class=_class)

    def login(self, *args, **credentials):
        return _Login(self, *args, **credentials)

    def get(self, url_name, *args, **kwargs):
        return self.request_json('get', url_name, *args, **kwargs)


class _Login(object):
    def __init__(self, test_case: LPTestCase, *args, **credentials):
        self.test_case = test_case
        if args and isinstance(args[0], User):
            email_field = getattr(User, 'EMAIL_FIELD', 'email')
            password_field = getattr(User, 'PASSWORD_FIELD', 'password')
            credentials.update({
                email_field: getattr(args[0], email_field),
                password_field: getattr(args[0], password_field),
            })

        if not credentials.get('password', False):
            credentials['password'] = 'password'

        token, _ = login_from_params(**credentials)
        self.test_case.current_token = token

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.test_case.current_token = None
