import fastapi
import time

MAX_TASK_COUNT=3

def mock_calculation(sleep_time:float=20):
    """
    mocking the heavy calculation of system optimization.


    """
    time.sleep(sleep_time)