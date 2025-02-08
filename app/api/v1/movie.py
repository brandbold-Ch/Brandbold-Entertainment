from os import path
from typing import AnyStr
from sqlmodel import Session
from app.config.sqlmodel_config import engine
from app.services.movie_service import MovieService
from flask import Blueprint, jsonify, request, Response
from app.utils.files_tools import (VIDEO_DIR,
                                   RESOURCES_DIR, THUMBNAIL_DIR, res_path)
from flask_jwt_extended import jwt_required

movie_bl = Blueprint("movie", __name__, url_prefix="/movies")
movie_services = MovieService(Session(engine))


@movie_bl.route("/thumbnail/<file>", methods=["GET"])
@jwt_required()
def thumbnail(file) -> Response:
    file_path = res_path(RESOURCES_DIR + THUMBNAIL_DIR + file)

    with open(file_path, "rb") as webp:
        webp_data = webp.read()

    return Response(
        webp_data,
        status=200,
        content_type="image/webp"
    )


@movie_bl.route("/stream/<file>", methods=["GET"])
@jwt_required()
def stream_video(file) -> Response:
    real_file = res_path(RESOURCES_DIR + VIDEO_DIR + file)
    file_size = path.getsize(real_file)
    range_header = request.headers.get("Range")

    if range_header:
        byte1, byte2 = range_header.replace("bytes=", "").split("-")
        start = int(byte1)
        end = int(byte2) if byte2 and byte2.isdigit() else file_size - 1
    else:
        start = 0
        end = file_size - 1

    return Response(
        get_chunks(real_file, start, end),
        status=206,
        mimetype="video/mp4",
        direct_passthrough=True,
        headers={
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(end - start + 1),
            "Connection": "keep-alive"
        }
    )


def get_chunks(video: str, start: int, end: int, chunk_size=8192) -> AnyStr:
    with open(video, "rb") as file:
        file.seek(start)
        while start < end:
            data = file.read(min(chunk_size, end - start + 1))
            if not data:
                break
            start += len(data)
            yield data


@movie_bl.route("/", methods=["GET"])
@jwt_required()
def get_movies() -> tuple[Response, int]:
    movies = movie_services.get_movies()
    movies_dict = [
        {
            **movie.model_dump(mode="json"),
            "video_url": f"{request.url}stream/{movie.video_url}",
            "thumbnail_url": f"{request.url}thumbnail/{movie.thumbnail_url}",
            "genres": [
                genre.model_dump(mode="json")
                for genre in movie.genres
            ],
            "franchises": [
                franchise.model_dump(mode="json")
                for franchise in movie.franchises
            ]
        }
        for movie in movies
    ]

    return jsonify(movies_dict), 200
