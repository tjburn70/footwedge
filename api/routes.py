import logging

from api.controllers import (
    auth,
    health,
    user,
)

logger = logging.getLogger(__name__)

ROUTES = {
    'api/auth': auth.blueprint,
    'api/health': health.blueprint,
    'api/user': user.blueprint,
}


def register(flask_app):
    for route, blueprint in ROUTES.items():
        try:
            flask_app.register_blueprint(blueprint, url_prefix=route)
        except Exception:
            logger.exception(f"Unable to register blueprint: '{blueprint.__name__}' to route: '{route}'")
