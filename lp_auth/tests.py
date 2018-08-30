from datetime import datetime

from django_dynamic_fixture import G

from lp_auth.models import User
from lp_auth.types import Token
from test_services.lp_test_case import LPTestCase


class AuthTestCase(LPTestCase):
    def test_login_fails_if_user_do_not_exists(self):
        self.post_json('auth_login', {'user_name': 'test', 'password': 'pass'})
        self.response_400()

    def test_login_gets_token_if_user_exists(self):
        user: User = G(User)
        self.post_json('auth_login', {'user_name': user.username, 'password': user.password})
        self.response_200()
        token: Token = self.get_content_json(_class=Token)

        self.assertEqual(token.user_id, user.id)
        self.assertGreater(token.expires_in, datetime.utcnow())
