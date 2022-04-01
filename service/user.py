import base64
import hashlib

from helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64decode(hash_digest).decode('utf-8')

    def compare_passwords(self, password_hash, other_password):
        is_true = password_hash == other_password
        return is_true

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        return self.dao.create(data=data)

    def update(self, data):
        user = self.get_one(data["id"])
        user.username = data.get("username")
        user.password = data.get("password")
        user.role = data.get("role")

        self.dao.update(user=user)

        return self.dao

    def delete(self, uid):
        user = self.get_one(uid)
        self.dao.delete(user=user)
