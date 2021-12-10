from celery import shared_task

from core.models import News


@shared_task(bind=True)
def reset_upvote(self):
    News.objects.all().update(up_votes=0)
