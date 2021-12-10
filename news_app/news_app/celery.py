import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_app.settings")

app = Celery("news_app")
app.conf.enable_utc = True
# app.conf.update(timezone='Asia/Baku')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.beat_schedule = {}
#     'update_result': {
#         'task': 'core.tasks.update_result',
#         'schedule': 10,
#         'args': 'playstation 5'
#     }
# }


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
