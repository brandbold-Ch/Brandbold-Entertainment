from flask import Blueprint
from app.services.user_services import UserServices

auth_bl = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bl.route("/login", methods=["POST"])
def login():
    ...
