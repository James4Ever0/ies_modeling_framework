import fastapi
import time
from test_server_client_configs import *


def mock_calculation(sleep_time:float=20):
    """
    Mocking the heavy calculation of system optimization.

    Args:
        sleep_time (float): the duration of our fake task, in seconds
    """
    time.sleep(sleep_time)

