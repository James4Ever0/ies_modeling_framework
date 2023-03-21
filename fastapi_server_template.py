## suggestion: use fastapi for self-documented server, use cerely for task management.

## question: how to convert pydantic models to json?

port = 9870

appName = "IES Optim Server Template"
version = "0.0.1"
tags_metadata = []
description = """
This server provides APIs for IES System Simulation & Optimization.
"""


from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI(description=description, version=version, tags_metadata=tags_metadata)


@app.post("/items/")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
