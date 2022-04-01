from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from helpers.decorators import auth_required, admin_required

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data = request.json
        director_service.create(data)
        return "", 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    @auth_required
    def get(self, did):
        try:
            director = director_service.get_one(did)
            return DirectorSchema().dump(director), 200
        except Exception:
            return "", 404

    @admin_required
    def put(self, did):
        try:
            data = request.json
            if "id" not in data:
                data["id"] = did
            director_service.update(data)
            return "", 204
        except Exception:
            return "", 404

    @admin_required
    def delete(self, did):
        try:
            director_service.delete(did)
            return "", 204
        except Exception:
            return "", 404
