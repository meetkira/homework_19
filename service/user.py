import hashlib

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_hash(password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def get_one(self, uid):
        return self.dao.get_one(uid)

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
