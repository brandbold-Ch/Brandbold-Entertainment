from datetime import timedelta
from flask import Blueprint, request, jsonify, Response
from sqlmodel import Session
from app.config.sqlmodel_config import engine
from app.exceptions.exceptions import JsonInvalidDataTypeException
from app.services import AuthService
from flask_jwt_extended import create_access_token

auth_bl = Blueprint("auth", __name__, url_prefix="/auth")
auth_service = AuthService(Session(engine))


@auth_bl.route("/login", methods=["POST"])
def login() -> tuple[Response, int]:
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        raise JsonInvalidDataTypeException(
            "There seems to be an error in your fields")

    user = auth_service.get_auth(username, password)
    token = create_access_token(
        identity=user["id"],
        expires_delta=timedelta(days=2)
    )

    return jsonify({
        "access_token": token,
        "data": user}), 200
