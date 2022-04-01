import calendar
import datetime
import hmac

import jwt
from flask import abort

from constants import SECRET, ALGO
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(401)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

        data = {
            "username": user.username,
            "role": user.role
        }
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=ALGO)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def approve_refresh_token(self, refresh_token):

        try:
            data = jwt.decode(refresh_token, SECRET, algorithms=[ALGO])
        except Exception:
            raise abort(401)

        username = data.get("username")

        return self.generate_tokens(username, None, is_refresh=True)
