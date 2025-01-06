from flask import Flask
from app.admin.views import admin_bl

app = Flask(__name__)
app.register_blueprint(admin_bl)


app.run(debug=True, host="0.0.0.0", port=8080)
