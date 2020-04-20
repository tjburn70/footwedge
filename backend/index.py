from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from backend.api import config, routes, version_info


def create_app(app_settings):
    app_name = app_settings.APP_NAME or __name__
    flask_app = Flask(app_name)
    flask_app.config.from_object(app_settings)
    routes.register(flask_app)
    return flask_app


app = create_app(config.FlaskConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/api')
def index():
    return version_info


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)
