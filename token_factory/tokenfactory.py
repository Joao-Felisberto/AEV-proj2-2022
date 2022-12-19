import os

import jwt
from flask import abort


class TokenFactory:
    def __init__(self):
        self.key = os.urandom(50).hex()

    def generate_token(self, username):

        encoded = jwt.encode(
            {
                'username': username,
                'admin': False
            },
            self.key,
            algorithm='HS256'
        )

        return encoded

    def token_verify(self, token):
        try:
            token_decode = jwt.decode(
                token,
                self.key,
                algorithms='HS256'
            )

            return token_decode
        except jwt.PyJWTError:
            return abort(400, 'Invalid token!')
