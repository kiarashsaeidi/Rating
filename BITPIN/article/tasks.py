from celery import shared_task
from .utils import process_post_ratings

@shared_task
def process_ratings_task():
    process_post_ratings()
