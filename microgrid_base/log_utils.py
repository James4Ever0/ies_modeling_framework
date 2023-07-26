"""
To use 'managed' loggers, you must import 'logger' from this file and pass it to other code.
"""

# TODO: use `code_checker.py` to insert `log_utils` dependency to every py file under this folder. except for this one!

import logging
import schedule

# ft = logging.Filter("myfilter") # default filter is just a string checker
allow_logging = True
allow_huge_logging=True
HUGE_MSG_THRESHOLD = 100

def refresh_logger_lock():
    global allow_logging
    allow_logging = True


def refresh_huge_logger_lock():
    global allow_huge_logging
    allow_huge_logging = True

schedule.every(0.3).seconds.do(refresh_logger_lock)
schedule.every(1).seconds.do(refresh_huge_logger_lock)


# class MessageLengthAndFrequencyFilter:
    
#     @staticmethod
def messageLengthAndFrequencyFilter(record: logging.LogRecord):
    # def filter(record: logging.LogRecord):
    global allow_logging, allow_huge_logging, HUGE_MSG_THRESHOLD
    schedule.run_pending()
    # print(dir(record))
    accepted = False
    msg = record.msg

    if len(msg) < HUGE_MSG_THRESHOLD:
        if allow_logging: # then this is some short message.
            accepted=True
            allow_logging=False
    else:
        if allow_huge_logging:
            record.msg = " ".join([msg[:HUGE_MSG_THRESHOLD], "..."])
            accepted = True
            allow_huge_logging = False
    return accepted


from logging import StreamHandler
import sys
import os

log_dir = os.path.join(os.path.dirname(__file__), "logs")

if os.path.exists(log_dir):
    if not os.path.isdir(log_dir):
        raise Exception(f"Non-directory object taking place of log directory `{log_dir}`.")
else:
    os.mkdir(log_dir)

log_filename = os.path.join(log_dir, "debug.log")

from logging.handlers import RotatingFileHandler

myHandler = RotatingFileHandler(
    log_filename, maxBytes=1024 * 1024 * 15, backupCount=3, encoding="utf-8"
)
myHandler.setLevel(logging.DEBUG)
# myHandler.setLevel(logging.INFO) # will it log less things? yes.
FORMAT = (
    "<%(name)s:%(levelname)s> [%(pathname)s:%(lineno)s - %(funcName)s()] %(message)s"
)
# FORMAT = "<%(name)s:%(levelname)s> [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
myFormatter = logging.Formatter(fmt=FORMAT)
myHandler.setFormatter(myFormatter)

stdout_handler = StreamHandler(sys.stdout)  # test with this!
stdout_handler.setLevel(logging.DEBUG)
# stdout_handler.addFilter(MessageLengthAndFrequencyFilter)
stdout_handler.addFilter(messageLengthAndFrequencyFilter) # method also works!
stdout_handler.setFormatter(myFormatter)
# do not use default logger!
# logger = logging.getLogger(__name__)
logger = logging.getLogger("microgrid")
logger.setLevel("DEBUG")
logger.addHandler(stdout_handler)
logger.addHandler(myHandler)

from rich.pretty import pretty_repr

def logger_print(*args):
    format_string = "\n\n".join(["%s"]*len(args))
    logger.debug(format_string, *[pretty_repr(arg) for arg in args])

logger_print("START LOGGING AT: {}".center("_", 100)
# logging.basicConfig(
#     # filename=filename,
#     # level=logging.getLogger().getEffectiveLevel(),
#     level="DEBUG",
#     # stream=sys.stderr
#     force=True, # overridding root logger, which is deprecated.
#     handlers=[stdout_handler],
# )

if __name__ == "__main__": # just a test.
    import time
    for i in range(100):
        time.sleep(0.1)
        logger.debug(f"test debug message {i}")
        logger.debug(f"test huge message {i} "*100) # huge mssage