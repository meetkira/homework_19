from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from implemented import movie_service

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
        }
        all_movies = movie_service.get_all(filters)
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        try:
            movie = movie_service.get_one(mid)
            return MovieSchema().dump(movie), 200
        except Exception:
            return "", 404

    def put(self, mid):
        try:
            data = request.json
            if "id" not in data:
                data["id"] = mid
            movie_service.update(data)
            return "", 204
        except Exception:
            return "", 404

    def delete(self, mid):
        try:
            movie_service.delete(mid)
            return "", 204
        except Exception:
            return "", 404
