from flask import Flask
from flask_cors import CORS

from api import version_info
from api import routes, config
from api.controllers.auth import jwt
from api.database import db_session


def create_app(app_settings):
    app_name = app_settings.APP_NAME or __name__
    flask_app = Flask(app_name)
    flask_app.config.from_object(app_settings)
    jwt.init_app(app=flask_app)
    routes.register(flask_app)
    return flask_app


app = create_app(config.FlaskConfig)
CORS(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/api')
def index():
    return version_info


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)
