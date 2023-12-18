from typing import Iterable

from celery import current_app as current_celery_app, Celery


def create_celery(tasks: Iterable[str]) -> Celery:
    celery_app: Celery = current_celery_app
    celery_app.config_from_object('src.celery_impl.celeryconfig')
    celery_app.autodiscover_tasks(tasks)
    return celery_app
