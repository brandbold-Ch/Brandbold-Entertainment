from os import path, remove
from werkzeug.datastructures import FileStorage
from app.exceptions.exceptions import *
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
        case _:
            raise ValueError(f"Formato de video no soportado: {content}")


def save_thumbnail(file: FileStorage, file_name: str) -> str:
    try:
        file_path = res_path(RESOURCES_DIR + THUMBNAIL_DIR + file_name + ".webp")

        with Image.open(file.stream) as image:
            image.save(file_path, format="WEBP", lossless=True)

        return file_name + ".webp"

    except Exception as e:
        raise RuntimeError(f"Error al guardar la miniatura: {str(e)}")


def save_movie(file: FileStorage, file_name: str) -> str:
    try:
        end = select_format(file.content_type)
        file_path = res_path(RESOURCES_DIR + VIDEO_DIR + file_name + end)

        with open(file_path, "wb") as movie:
            movie.write(file.stream.read())

        return file_name + end

    except ValueError as e:
        raise ValueException(e.__repr__())

    except Exception as e:
        raise GenericException(e.__repr__())


def delete_video(file: str) -> None:
    try:
        file_path = res_path(RESOURCES_DIR + VIDEO_DIR + file)

        if not path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file} no existe.")

        remove(file_path)

    except FileNotFoundError as e:
        raise FileNotFoundException(e.__repr__())
    except Exception as e:
        raise GenericException(e.__repr__())


def delete_thumbnail(file: str) -> None:
    try:
        file_path = res_path(RESOURCES_DIR + THUMBNAIL_DIR + file)
        if not path.exists(file_path):
            raise FileNotFoundError("File Not Found")

        remove(file_path)

    except FileNotFoundError as e:
        raise FileNotFoundException(e.__repr__())
    except Exception as e:
        raise GenericException(e.__repr__())
