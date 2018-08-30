from django_dynamic_fixture import G

from lp_auth.models import User
from test_services.lp_test_case import LPTestCase


class CardsTestCase(LPTestCase):
    def test_cards_works_only_with_logged_user(self):
        user = G(User)
        with self.login(user):
            self.get('cards_index')
            self.response_200()
