# confusing.
def class_method_decorator(func):  # what will be passed to the function?
    def decorated_func(self: object, *args, **kwargs):
        # class_instance = args[0] # <- this is the 'self'
        # really?
        print("CLASS INSTANCE:", self)
        print("ALL REMAINING ARGS:", args)
        print("ALL KWARGS:", kwargs)
        print("___BEFORE INVOKE___")
        value = func(self, *args, **kwargs)
        print("___AFTER INVOKE___")
        return value

    return decorated_func


class A:
    def __init__(self, param):
        self.param = param

    # cannot use self here. warning!

    @class_method_decorator
    def class_method(self, param_0):
        print("PASSED PARAM_0:", param_0)
        print("CLASS ATTR PARAM:", self.param)


a = A("[PARAM]")
a.class_method("[PARAM_0]")
