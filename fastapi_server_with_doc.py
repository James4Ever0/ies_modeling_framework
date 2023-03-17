# test to create a server with fastapi, generate doc automatically.
# code from: https://fastapi.tiangolo.com/tutorial/metadata/

from fastapi import FastAPI, HTTPException
AppName = "ChimichangApp"
description = f"""
{AppName} API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
""" # this is not docstring. this is passed as parameter.

app = FastAPI(
    title=AppName,
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    }, # contact?
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None
inventory = []
@app.post("/items/")
async def create_item(item: Item):
    """
    Create a new item.
    ## Parameters
    - **item**: Item object to create.
    ## Returns
    The created item.
    ## Errors
    - **400 Bad Request**: Invalid request data.
    """
    if item.name == "foo":
        raise HTTPException(status_code=400, detail="Item name cannot be foo.")
    inventory.append(item)
    return item

# how to generate doc?
# visit: http://<host_ip>:9981/docs
#
# how to export doc?
#
# By default, the OpenAPI schema is served at /openapi.json
# what is that json anyway?

port = 9981

import uvicorn

uvicorn.run(app, host='0.0.0.0' ,port=port)
