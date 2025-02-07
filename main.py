from flask import Flask
from app.api.v1.admin import admin_bl
from app.api.v1.movie import movie_bl
from app.api.v1.genre import genre_bl
from app.api.v1.auth import auth_bl
from app.api.v1.user import user_bl
from app.exceptions.exceptions import BaseServerException
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 7 * 1024 * 1024 * 1024  # 5 GB
jwt = JWTManager(app)


@app.errorhandler(BaseServerException)
def handle_errors(error):
    return error.to_dict()


app.register_blueprint(admin_bl)
app.register_blueprint(movie_bl)
app.register_blueprint(genre_bl)
app.register_blueprint(auth_bl)
app.register_blueprint(user_bl)

app.run(debug=True, host="0.0.0.0", port=8080)
