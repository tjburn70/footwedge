from decimal import Decimal

from celery import Celery

from api.models import (
    GolfRound,
    TeeBox,
    Handicap
)
from api import index


class CeleryConfig:
    broker_url = 'redis://localhost:6379/1'
    result_backend = 'redis://localhost:6379/1'
    task_serializer = 'pickle'
    result_serializer = 'json'
    accept_content = ['json', 'pickle']
    enable_utc = True
    worker_concurrency = 5
    task_compression = 'gzip'
    task_acks_late = True
    worker_prefetch_multiplier = 1
    worker_max_tasks_per_child = 500


celery_app = Celery('tasks')
celery_app.config_from_object(CeleryConfig)


def calculate_differential(gross_score, course_rating, slope):
    differential = ((gross_score - course_rating) * 113) / slope
    return differential


def sample_size(num_rounds: int):
    if num_rounds < 5:
        print('sample size is too small, need atleast 5 rounds recorded')
        return
    if num_rounds <= 10:
        size = 1
    elif num_rounds <= 19:
        size = 5
    else:
        size = 10

    return size


def determine_lowest_differentials(differentials, size):
    num_differentials = len(differentials)
    if size > num_differentials:
        raise Exception('Size greater than the number of differentials')
    elif size == num_differentials:
        return differentials
    else:
        sorted_differentials = sorted(differentials)
        lowest_differentials = sorted_differentials[:size]
        return lowest_differentials


def handicap(differentials):
    size = sample_size(num_rounds=len(differentials))
    lowest_differentials = determine_lowest_differentials(
        differentials=differentials,
        size=size,
    )
    return (sum(lowest_differentials)/len(lowest_differentials)) * Decimal('0.96')


@celery_app.task
def calculate_usga_handicap(*args, **kwargs):
    user_id, *_ = args
    differentials = []
    with index.app.app_context():
        ordered_golf_rounds = GolfRound.get_by_user_id(user_id=user_id)
        if len(ordered_golf_rounds) > 20:
            golf_rounds = ordered_golf_rounds[:20]
        else:
            golf_rounds = ordered_golf_rounds

        for golf_round in golf_rounds:
            tee_box = TeeBox.get_by_id(tee_box_id=golf_round.tee_box_id)
            differential = calculate_differential(
                gross_score=golf_round.gross_score,
                course_rating=tee_box.course_rating,
                slope=tee_box.slope,
            )
            differentials.append(differential)

        handicap_index = handicap(differentials=differentials)

        current_handicap = Handicap.get_active(user_id=user_id)
        if current_handicap:
            current_handicap.close()

        Handicap(
            user_id=user_id,
            index=handicap_index,
            authorized_association='USGA'
        ).save()
