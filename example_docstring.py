"""
a 狗 that will bark.
"""
from typing import List

# pdoc is different than pdoc3.
# where's the search box?

global_var2 = None
"""
some other global variable
"""

global_var = None
"""
some global variable2 _Default to None_
"""

def some_random_method(param_1:str,param_2, kw_param_1=None) -> None:
    #: Documentation comment for class_variable
    #: spanning over three lines.
    """_just a random method_

    Args:
        param_1 (str): _parameter at position 1_
        param_2 (str): _parameter at position 2_
        kw_param_1 (Any, optional): _keyword parameter 1_.  NO LATEX SUPPORT?
    
    Return:
        Nothing returned.
        
    Note:
        Extra Notes?
        ```
        import os
        os.system("ls -lth")
        ```
    """

class Dog:
    """dog class"""
    name: str
    """The name of our dog."""
    friends: List["Dog"]
    """The friends of our dog."""

    def __init__(self, name: str):
        """Make a Dog without any friends (yet)."""
        self.name = name
        self.friends = []

    def bark(self, loud: bool = True):
        """*woof*"""

if __name__ == "__main__":
    """main job goes here"""
    var_1 = None
    """variable 1 set to None"""
    var_2 = 1
    """var 2 set to 1"""
    print("finished")
    """denote we are finished"""