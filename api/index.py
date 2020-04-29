from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from api import version_info
from api import routes, config
from api.controllers.auth import jwt
from api.models import db


def create_app(app_settings):
    app_name = app_settings.APP_NAME or __name__
    flask_app = Flask(app_name)
    flask_app.config.from_object(app_settings)
    jwt.init_app(app=flask_app)
    db.init_app(app=flask_app)
    routes.register(flask_app)
    return flask_app


app = create_app(config.FlaskConfig)
CORS(app)
migrate = Migrate(app, db)


@app.route('/api')
def index():
    return version_info


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)
