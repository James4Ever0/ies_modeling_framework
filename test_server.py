import fastapi
import time

def mock_calculation(sleep_time:float=20):
    time.sleep(sleep_time)