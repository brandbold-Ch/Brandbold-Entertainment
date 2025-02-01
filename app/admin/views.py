from flask import Blueprint, render_template, request, redirect, url_for, jsonify, Response, make_response
from uuid import uuid4
from os import path
from sqlmodel import Session
from werkzeug.datastructures import FileStorage
from config.sqlmodel_config import engine
from services.movie_service import MovieService
from exceptions.exceptions import BaseServerException

admin_bl = Blueprint("admin", __name__,
                     url_prefix="/admin", template_folder="templates")
movie_services = MovieService(Session(engine))

RESOURCES_DIR = "../../../static"
THUMBNAIL_DIR = "thumbnail"
MOVIES_DIR = "movies"
THUMBNAIL_EXT = "webp"


def res_path(file: str, _type: str, _dir: str) -> str:
    filename = f"{RESOURCES_DIR}/{_dir}/{file}.{_type}"
    return path.abspath(path.join(__file__, filename))


def select_format(content: str) -> str:
    match content:
        case "video/mp4":
            return "mp4"
        case "video/x-matroska":
            return "mkv"
        case "video/webm":
            return "webm"
        case "video/ogg":
            return "ogg"
        case "video/avi":
            return "avi"


def save_file(file: FileStorage, filename: str, extension: str, directory: str) -> None:
    file_path = res_path(filename, extension, directory)
    with open(file_path, "wb") as f:
        f.write(file.read())


@admin_bl.errorhandler(BaseServerException)
def handle_generic_error(error):
    return error.to_dict()


@admin_bl.route("/delete_movie/<uuid:movie_id>", methods=["DELETE"])
def delete_movie(movie_id) -> Response:
    movie_services.del_movie(movie_id)
    return jsonify({"message": "Película Eliminada Correctamente"})


@admin_bl.route("/", methods=["GET"])
def dashboard() -> str:
    return render_template("dashboard.html")


@admin_bl.route("/movie_list", methods=["GET"])
def movie_list() -> str:
    movies = movie_services.get_movies()
    return render_template("movie_list.html", data=movies)


@admin_bl.route("/update_movie/<movie_data>", methods=["GET"])
def update_movie(movie_data) -> str:
    return render_template("update_movie.html", data=movie_data)


@admin_bl.route("/upload_movie", methods=["GET", "POST"])
def upload_movie() -> str:
    if request.method == "POST":
        movie_file: FileStorage = request.files.get("video_url")
        thumb_file: FileStorage = request.files.get("thumbnail_url")
        generic_name = str(uuid4())

        video_format = select_format(movie_file.content_type)
        save_file(thumb_file, generic_name, THUMBNAIL_EXT, THUMBNAIL_DIR)
        save_file(movie_file, generic_name, video_format, MOVIES_DIR)

        data = request.form.to_dict()
        data.update({"thumbnail_url": f"{generic_name}.{THUMBNAIL_EXT}"})
        data.update({"video_url": f"{generic_name}.{video_format}"})

        movie_services.add_movie(**data)

    return render_template("upload_movie.html")


@admin_bl.route("/user_list", methods=["GET", "POST"])
def user_list() -> str:
    return render_template("user_list.html")


@admin_bl.route("/video_streaming/<movie_path>", methods=["GET"])
def video_streaming(movie_path: str) -> str:
    return render_template("video_streaming.html", file=movie_path)
