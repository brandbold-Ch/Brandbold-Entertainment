from app.config.sqlmodel_config import engine
from flask import Blueprint, request, jsonify, Response
from app.exceptions.exceptions import DataValidationException
from sqlmodel import Session
from app.services import UserServices

user_bl = Blueprint("user", __name__, url_prefix="/users")
user_service = UserServices(Session(engine))


@user_bl.route("/", methods=["POST"])
def create_user() -> tuple[Response, int]:
    data = request.get_json()

    if "user" not in data or "auth" not in data:
        raise DataValidationException("Don't found user key or auth key")

    result = (user_service
              .create_user(data["user"], data["auth"]))
    return jsonify(result), 201
