import logging

from api.controllers import (
    auth,
    health,
    user,
    handicap,
    golf_round,
    golf_club,
    golf_course,
)

logger = logging.getLogger(__name__)

ROUTES = {
    '/api/auth': auth.blueprint,
    '/api/health': health.blueprint,
    '/api/user': user.blueprint,
    '/api/handicaps': handicap.blueprint,
    '/api/golf-rounds': golf_round.blueprint,
    '/api/golf-clubs': golf_club.blueprint,
    '/api/golf-courses': golf_course.blueprint,
}


def register(flask_app):
    for route, blueprint in ROUTES.items():
        try:
            flask_app.register_blueprint(blueprint, url_prefix=route)
        except Exception:
            logger.exception(f"Unable to register blueprint: '{blueprint.__name__}' to route: '{route}'")
