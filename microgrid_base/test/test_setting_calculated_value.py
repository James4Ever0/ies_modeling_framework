from pydantic import BaseModel, validator
class A(BaseModel):
    a :int = 1
    b:str
    @validator('b')
    def validate_b(cls, v, values):
            values['a'] = 2 # working.
            return v


b = A(b='a')
print(b)