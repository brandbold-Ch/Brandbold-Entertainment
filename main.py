from flask import Flask, jsonify, Response
from app.api.v1.admin import admin_bl
from app.api.v1.movie import movie_bl
from app.api.v1.genre import genre_bl
from app.api.v1.auth import auth_bl
from app.api.v1.user import user_bl
from app.exceptions.exceptions import BaseExceptionError, InvalidTokenException, ExpiredTokenException, \
    NotFoundTokenException
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 7 * 1024 * 1024 * 1024
app.config["SECRET_KEY"] = "my_secret"
app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]

jwt = JWTManager(app)


@app.errorhandler(BaseExceptionError)
def handle_errors(error: BaseExceptionError) -> tuple[Response, int]:
    return jsonify(error.to_dict()), error.http_code


@jwt.invalid_token_loader
def invalid_token_cb(error) -> tuple[Response, int]:
    exc = InvalidTokenException(error.__repr__())
    return jsonify(exc.to_dict()), exc.http_code


@jwt.expired_token_loader
def expired_token_cb(jwt_header, jwt_payload) -> tuple[Response, int]:
    exc = ExpiredTokenException("Expired Token")
    return jsonify(exc.to_dict()), exc.http_code


@jwt.unauthorized_loader
def missing_token_cb(error) -> tuple[Response, int]:
    exc = NotFoundTokenException(error.__repr__())
    return jsonify(exc.to_dict()), exc.http_code


app.register_blueprint(admin_bl)
app.register_blueprint(movie_bl)
app.register_blueprint(genre_bl)
app.register_blueprint(auth_bl)
app.register_blueprint(user_bl)

#app.run(debug=True, host="0.0.0.0", port=8080)
