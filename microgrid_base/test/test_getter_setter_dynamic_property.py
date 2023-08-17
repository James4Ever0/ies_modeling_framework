from functools import partial
class TestClass:
    __slots__ = ['prop']
    def __init__(self):...
    # there's no "getter/setter" factory method.

tc = TestClass()
print(tc.prop) # unbound.
tc.prop = 1
print(tc.prop)
tc.p = 1 # great.