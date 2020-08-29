import logging

from api.controllers import (
    auth,
    health,
    handicap,
    user,
    golf_club,
    golf_course,
    search,
)

logger = logging.getLogger(__name__)

ROUTES = {
    '/api/auth': auth.blueprint,
    '/api/health': health.blueprint,
    '/api/handicaps': handicap.blueprint,
    '/api/user': user.blueprint,
    '/api/golf-clubs': golf_club.blueprint,
    '/api/golf-courses': golf_course.blueprint,
    '/api/search': search.blueprint,
}


def register(flask_app):
    for route, blueprint in ROUTES.items():
        try:
            flask_app.register_blueprint(blueprint, url_prefix=route)
        except Exception:
            logger.exception(f"Unable to register blueprint: '{blueprint.__name__}' to route: '{route}'")
