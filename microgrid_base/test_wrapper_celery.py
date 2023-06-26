from test_wrapper import MAIN_NAME, app

function_id = f"{MAIN_NAME}.mfunc"
# from celery.result import AsyncResult
task = app.send_task(function_id)
# installed stub: pip install celery-types
# task:AsyncResult = app.send_task(function_id)

import time
import rich

while True:
    time.sleep(1)
    print("STATUS?", task.status)
    # print(dir(task), type(task))
    rich.print(task.__dict__)
    