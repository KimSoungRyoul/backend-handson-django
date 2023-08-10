from time import sleep

from config.celery import app


@app.task(bind=True)
def debug_task(sleep_cnt):
    sleep(sleep_cnt)
    print("Request: 김성렬")
