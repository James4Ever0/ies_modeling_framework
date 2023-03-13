from fastapi import FastAPI
import time
from test_server_client_configs import *

def mock_calculation(sleep_time:float=20):
    """
    Mocking the heavy calculation of system optimization.

    Args:
        sleep_time (float): the duration of our fake task, in seconds
    """
    time.sleep(sleep_time)

app = FastAPI()
# where is the port?

@app.post()
def run_sync():
    ...

@app.post()
def run_async():
    ...

@app.post()
def get_result_async():
    ...

import uvicorn

uvicorn.run(app,port=port)