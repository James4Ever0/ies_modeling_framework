from log_utils import logger_print

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
    logger_print("STATUS?", task.status)
    # logger_print(dir(task), type(task))
    logger_print(task.__dict__)
    