from Utility import store_data_to_redis
from .celery import app


@app.task
def refresh_data():
    store_data_to_redis()