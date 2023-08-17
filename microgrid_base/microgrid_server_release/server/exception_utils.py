from log_utils import logger_print

from beartype import beartype
@beartype
class ExceptionManager:
    def __init__(self):
        self.errors = []
    def __bool__(self):
        return len(self.errors)>0
    def has_exception(self):
        return bool(self)
    def append(self, error:str):
        self.errors.append(error)
    def clear(self):
        self.errors = []
    def format_error(self, clear=True, join:str="\n"):
        error_msg = join.join(self.errors)
        if clear:
            self.clear()
        return error_msg
    def raise_if_any(self):
        if self.errors:
            raise Exception(self.format_error())
    def print_if_any(self):
        if self.errors:
            logger_print(self.format_error())
            return True
        return False
    def __enter__(self):
        self.raise_if_any()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        # does not try to suppress exceptions (return True if exception)
        self.print_if_any()
    def __str__(self):
        return self.format_error(clear=False)
    def __repr__(self):
        return self.format_error(clear=False)
    def __len__(self):
        return len(self.errors)
    def __iter__(self):
        return iter(self.errors)
    

exceptionManager = ExceptionManager()