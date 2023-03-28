from fastapi import FastAPI, BackgroundTasks

# do not import the function. import the celery app.
from celery_test import app as celery_app

app = FastAPI()
# import logging

# log = logging.getLogger(__name__)
# do not use logging?

def celery_on_message(body):
    print("BODY TYPE?", type(body))
    print("ON MESSAGE?",body)


def background_on_message(task):
    value = task.get(on_message=celery_on_message, propagate=False)
    print("VALUE TYPE?", type(value)) # str, '14'
    print("TASK VALUE?", value)
# backend does not support on_message callback?

@app.get("/add/{a}/{b}")
def add_get(a, b, background_task: BackgroundTasks):
    # apparently it is not calling celery.
    # val = add(a,b)
    args = [a, b]
    task_name = "tasks.add" # working?
    task = celery_app.send_task(task_name, args=args)
    print("PENDING CELERY TASK:", task)
    background_task.add_task(background_on_message, task)
    return "RECEIVED"


import uvicorn

uvicorn.run(app, host="127.0.0.1", port=8010)
