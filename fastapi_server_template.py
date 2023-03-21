
## suggestion: use fastapi for self-documented server, use cerely for task management.

## question: how to convert pydantic models to json?

port = 9870

appName = "IES Optim Server Template"

description="""
This server provides APIs for IES System Optimization.
"""

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result