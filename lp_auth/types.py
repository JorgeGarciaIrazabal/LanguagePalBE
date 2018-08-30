from datetime import datetime

import jwt
from ajson import AJson, ASerializer

from language_pal_be.settings import JWT_SECRET_KEY


@AJson()
class LoginBody(object):
    email: str  # @aj(required)
    password: str  # @aj(required)


@AJson()
class DecodedToken:
    expires_in: datetime
    user_id: int


@AJson()
class Token(object):
    token: str

    @property
    def user_id(self) -> int:
        return ASerializer().from_dict(self._decode_token(), DecodedToken).user_id

    @property
    def expires_in(self) -> datetime:
        return ASerializer().from_dict(self._decode_token(), DecodedToken).expires_in

    def _decode_token(self):
        return jwt.decode(self.token, JWT_SECRET_KEY)
