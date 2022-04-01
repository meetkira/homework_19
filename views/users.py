from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        users = user_service.get_all()
        res = UserSchema(many=True).dump(users)
        return res, 200

    def post(self):
        data = request.json
        user_service.create(data)
        return "", 201


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        try:
            user = user_service.get_one(uid)
            return UserSchema().dump(user), 200
        except Exception:
            return "", 404

    def put(self, uid):
        try:
            data = request.json
            if "id" not in data:
                data["id"] = uid
            user_service.update(data)
            return "", 204
        except Exception:
            return "", 404

    def delete(self, uid):
        try:
            user_service.delete(uid)
            return "", 204
        except Exception:
            return "", 404
