import enum

class A(enum.Enum):
    MEMBER1 = 'member1'
    MEMBER2 = 'member2'

class B(enum.Enum):
    MEMBER3 = 'member3'
    MEMBER4 = 'member4'

    # Define a mapping between B's members and A's members
    _mapping = {
        'member3': A.MEMBER1,
        'member4': A.MEMBER2,
    }

    def __new__(cls, value):
        # Check if the value is in B's mapping
        # breakpoint()
        if value in cls._mapping:
            # If so, return the corresponding member from A
            return cls._mapping[value]
        # Otherwise, create a new member in B
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

print(list(A))  # [<A.MEMBER1: 'member1'>, <A.MEMBER2: 'member2'>]
print(list(B))  # [<A.MEMBER1: 'member3'>, <A.MEMBER2: 'member4'>]
