"""
a dog that will bark.
"""
from typing import List


global_var = None
"""
some global variable
"""

def some_random_method()

class Dog:
    """🐕"""
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