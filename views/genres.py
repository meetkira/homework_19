from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service
from helpers.decorators import auth_required, admin_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data = request.json
        genre_service.create(data)
        return "", 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        try:
            genre = genre_service.get_one(gid)
            return GenreSchema().dump(genre), 200
        except Exception:
            return "", 404

    @admin_required
    def put(self, gid):
        try:
            data = request.json
            if "id" not in data:
                data["id"] = gid
            genre_service.update(data)
            return "", 204
        except Exception:
            return "", 404

    @admin_required
    def delete(self, gid):
        try:
            genre_service.delete(gid)
            return "", 204
        except Exception:
            return "", 404
