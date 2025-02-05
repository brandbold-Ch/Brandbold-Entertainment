from flask import Flask
from app.api.v1.admin import admin_bl
from app.api.v1.movie import movie_bl
from app.exceptions.exceptions import BaseServerException

app = Flask(__name__)


@app.errorhandler(BaseServerException)
def handle_errors(error):
    return error.to_dict()


app.register_blueprint(admin_bl)
app.register_blueprint(movie_bl)


app.run(debug=True, host="0.0.0.0", port=8080)
