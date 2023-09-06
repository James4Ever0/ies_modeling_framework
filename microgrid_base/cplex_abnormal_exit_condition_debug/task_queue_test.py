# rq huey taskiq tasktiger
from task_queue import task_fail, task_success
rlist = []

for task in [task_fail, task_success]:
    r = task()
    rlist.append(r)

for r in rlist:
    ret = r(blocking=True, timeout=5)
    print('ret:', ret)