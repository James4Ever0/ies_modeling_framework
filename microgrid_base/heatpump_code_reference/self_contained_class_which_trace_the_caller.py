import inspect
# TODO: iterate components like piecewise functions, iterative constraints, indexed variables and bound each component to the line of code which creates them

def trace_frame_till_condition(frame, cond):
    if not cond(frame):
        return frame
    else:
        return trace_frame_till_condition(frame.f_back, cond)


class SelfContainedCallerTracer(object):
    """
    This class is used to trace calls to methods of a class.
    It is used to trace calls to methods of a class that are not
    called from other methods of the same class.
    """

    def __init__(self):
        self.cond = lambda f: isinstance(f.f_locals.get("self", None), self.__class__)

    def call(self):
        called_by = inspect.currentframe()
        # you can trace more info like the instance attributes of the caller
        called_by = trace_frame_till_condition(called_by, self.cond)
        # print(dir(called_by))
        # print(called_by)
        # breakpoint()
        print("-" * 60)
        print(f"method {self.__class__.__name__}.call called_by:", called_by)
        print(
            "file",
            repr(called_by.f_code.co_filename) + ",",
            "line",
            called_by.f_lineno,
        )
        print("caller:", called_by.f_code.co_name)
        # print("-"*60)

    def self_call(self):
        self.call()


# TODO: make sure child classes are somehow working properly
# TODO: using metaclass?


class ChildClass(SelfContainedCallerTracer):
    def __init__(self):
        sclass = SelfContainedCallerTracer
        non_magic_method_names = [n for n in dir(sclass) if not n.startswith("__")]
        self.cond = lambda f: f.f_code.co_name in non_magic_method_names

    def some_other(self):
        self.self_call()

    def just_call(self):
        self.call()


def call1():
    instance = SelfContainedCallerTracer()
    instance.call()
    instance.self_call()


def call2():
    instance = ChildClass()
    instance.some_other()
    instance.call()
    instance.just_call()
    instance.self_call()


if __name__ == "__main__":
    call1()
    call2()
    obj = SelfContainedCallerTracer()
    obj.call()
