from os import path, remove
from werkzeug.datastructures import FileStorage
from PIL import Image

RESOURCES_DIR = "../../../static/"
THUMBNAIL_DIR = "thumbnail/"
VIDEO_DIR = "movies/"


def res_path(filename: str) -> str:
    return path.abspath(path.join(__file__, filename))


def select_format(content: str) -> str:
    match content:
        case "video/mp4":
            return ".mp4"
        case "video/x-matroska":
            return ".mkv"
        case "video/webm":
            return ".webm"
        case "video/ogg":
            return ".ogg"
        case "video/avi":
            return ".avi"


def save_thumbnail(file: FileStorage, file_name: str) -> str:
    file_path = res_path(RESOURCES_DIR +
                         THUMBNAIL_DIR + file_name + ".webp")

    with Image.open(file.stream) as image:
        image.save(file_path, format="WEBP", lossless=True)
    return file_name + ".webp"


def save_movie(file: FileStorage, file_name: str) -> str:
    end = select_format(file.content_type)
    file_path = res_path(RESOURCES_DIR +
                         VIDEO_DIR + file_name + end)

    with open(file_path, "wb") as movie:
        movie.write(file.stream.read())

    return file_name + end


def delete_video(file) -> None:
    remove(res_path(RESOURCES_DIR +
                    VIDEO_DIR + file))


def delete_thumbnail(file) -> None:
    remove(res_path(RESOURCES_DIR +
                    THUMBNAIL_DIR + file))
