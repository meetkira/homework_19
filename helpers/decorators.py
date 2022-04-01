import jwt
from flask import request, abort

from helpers.constants import SECRET, ALGO


def auth_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]

        try:
            token_auth = data.split("Bearer ")[-1]
            jwt.decode(token_auth, SECRET, algorithms=[ALGO])
        except Exception as e:
            print("JWT decode exception", e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]

        try:
            token_auth = data.split("Bearer ")[-1]
            user = jwt.decode(token_auth, SECRET, algorithms=[ALGO])
            role = user.get("role", "user")
        except Exception as e:
            print("JWT decode exception", e)
            abort(401)

        if role != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper
