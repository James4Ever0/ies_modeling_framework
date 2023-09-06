# rq huey taskiq tasktiger
from task_queue import task_fail, task_success
rlist = []

# is there any callback?
r = task_fail()
r = task_success()
