from celery import Celery
from celery.schedules import crontab
import os


redis_url = os.environ.get("REDIS_URL", 'None')

app = Celery("app", broker=redis_url, backend=redis_url, include=["task"])

#  app.autodiscover_tasks()
app.conf.timezone = "Asia/Kolkata"

app.conf.beat_schedule = {
    "refresh-bhavcopy-data-in-redis": {
        "task": "app.tasks.refresh_data",
        "schedule": crontab(minute="30", hour="5", day_of_week="mon-fri"),
        "args": (),
    }
}

if __name__ == "__main__":
    app.start()