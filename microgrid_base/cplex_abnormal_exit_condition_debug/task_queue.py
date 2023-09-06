import time
import os

# it is best to use linux.
if os.name == "nt":
    import dill
    import multiprocessing.reduction as mred

    class ForkingPickler(dill.Pickler):
        """Pickler subclass used by multiprocessing."""

        _extra_reducers = {}
        _copyreg_dispatch_table = mred.copyreg.dispatch_table

        def __init__(self, *args):
            super().__init__(*args)
            self.dispatch_table = self._copyreg_dispatch_table.copy()
            self.dispatch_table.update(self._extra_reducers)

        @classmethod
        def register(cls, type, reduce):
            """Register a reduce function for a type."""
            cls._extra_reducers[type] = reduce

        @classmethod
        def dumps(cls, obj, protocol=None):
            buf = mred.io.BytesIO()
            cls(buf, protocol).dump(obj)
            return buf.getbuffer()

        loads = dill.loads

    mred.ForkingPickler = ForkingPickler

# warning! celery is more stable than these libs.
from huey import RedisHuey
import func_timeout
import retrying
# do not use SqliteHuey
huey = RedisHuey(port=6380)

# lambda decorator is evil.
# timeout_func = lambda timeout: (lambda func: func_timeout(timeout=timeout, func=func))


@huey.task()
@retrying.retry(stop_max_attempt_number=3) # usually this setup is not for our debugging tasks.
@func_timeout.func_set_timeout(3)
def task_success():
    print("running task success")
    time.sleep(1)
    print("end running task success")


@huey.task()
@retrying.retry(stop_max_attempt_number=3)
@func_timeout.func_set_timeout(3)
def task_fail():
    print("running task fail")
    time.sleep(7)
    print("end running task fail")
