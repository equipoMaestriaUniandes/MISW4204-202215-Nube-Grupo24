from celery import Celery

celery_app = Celery(__name__)


@celery_app.task()
def add_together(a, b):
    return a+b
