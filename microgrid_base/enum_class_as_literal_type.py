from enum import StrEnum
a = StrEnum('Color', ['RED', 'GREEN', 'BLUE'])
# from enum import Enum
# a = Enum('Color', ['RED', 'GREEN', 'BLUE'])

b: a = a.BLUE # Color.BLUE
print(b, type(b))
print(b == 'blue') # true