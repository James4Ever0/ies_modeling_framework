import json
from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
item = Item(name='test', price=9.99)
json_str = json.dumps(item.dict()) # working.
print(json_str)