
import inspect
# import ast
# import astor

from typing import List #, Union

# TODO: use metaclass instead of this!

class MethodRegistry(list):
    """
    A registry of methods, used to register methods with given signature.
    """

    def __init__(self, signature: List[str]):
    # def __init__(self, registry_name:str, signature: List[str]):
        # TODO: dynamically infer registry name
        # self.registry_name = registry_name
        # self.decorator_source = f"{self.registry_name}.register"
        self.signature = signature
        self.names = set()
        super().__init__()

    def check_signature(self, obj):
        obj_sig = inspect.signature(obj)
        obj_keys = list(obj_sig.parameters.keys())
        assert (
            obj_keys == self.signature
        ), "Signature mismatch: (registered signature: {}, given signature: {})".format(
            self.signature, obj_keys
        )
        return True

    def add(self, obj):
        if self.check_signature(obj):
            self.append(obj)

    def register(self, obj):
        self.add(obj)
        return obj
    
    # def collect(self):
    #     currentframe=inspect.currentframe()
    #     caller = currentframe.f_back
    #     for name, obj in caller.f_locals.items():
    #         if name not in self.names:
    #             test_passed = False
    #             try:
    #                 source = inspect.getsource(obj)
    #                 tree = ast.parse(source)
    #                 elem = tree.body[0]
    #                 # TODO: async function def
    #                 if isinstance(elem, Union[ast.AsyncFunctionDef,ast.FunctionDef]):
    #                     decs = elem.decorator_list
    #                     for d in decs:
    #                         dec_source = astor.to_source(d).strip()
    #                         # dec_source = ast.unparse(d)
    #                         # breakpoint()
    #                         if dec_source.endswith(self.decorator_source):
    #                             test_passed = True
    #             except:
    #                 pass
    #             if test_passed:
    #                 self.names.add(name)
    #                 self.add(obj)

failsafe_methods = MethodRegistry(["mw"])
# failsafe_methods = MethodRegistry("failsafe_methods",["mw"])

@failsafe_methods.register
def dummy_method(mw):
    ...


# failsafe_methods.collect()
print(failsafe_methods) # nothing!

# class MethodRegistryMetaclass(type):
#     def __new__(cls, name, bases):
#         ...

# class FailsafeMethodRegistry(metaclass = MethodRegistryMetaclass):
#     @staticmethod
#     def dummy_method(mw):
#         ...
