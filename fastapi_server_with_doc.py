# test to create a server with fastapi, generate doc automatically.
# code from: https://fastapi.tiangolo.com/tutorial/metadata/

# notice: after you've done developing server, you can generate client automatically.
# reference: https://fastapi.tiangolo.com/advanced/generate-clients/
# custom the way to generate client functions.

port = 9982

if __name__ == "__main__":
    from fastapi import FastAPI, HTTPException
    import rich

    AppName = "ChimichangApp"
    description = f"""
    {AppName} API helps you do awesome stuff. 🚀

    ## Items

    You can **read items**.

    ## Users

    You will be able to:

    * **Create users** (_not implemented_).
    * **Read users** (_not implemented_).
    """  # this is not docstring. this is passed as parameter.

    app = FastAPI(
        title=AppName,
        description=description,
        version="0.0.1",
        terms_of_service="http://example.com/terms/",
        contact={
            "name": "Deadpoolio the Amazing",
            "url": "http://x-force.example.com/contact/",
            "email": "dp@x-force.example.com",
        },  # contact?
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
    )

    @app.get(
        "/items/",
        response_description="get response example",
        summary="summary for get items",
    )  # what is dependencies anyway?
    async def read_items():
        return [{"name": "Katana"}]

    from pydantic import BaseModel
    from typing import Mapping

    class Item(BaseModel):
        """
        can this item thing have any schema description?
        """

        name: str
        price: float
        """
        how to insert mock data and data entry description?
        """
        is_offer: bool = None
        myDict: Mapping  # it is mapping, not dict.
        # if it is clear, you don't have to do this. if unclear, you do something different.

    inventory = []

    class ResponseModel(BaseModel):
        ans: str
        ans_1: str

    # when it is async, no parallelism!
    # but who needs that?
    @app.post(
        "/items/",
        description="api for creating an item",
        response_description="respond if creation is successful.",
        response_model=ResponseModel,
    )
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
        print("RECV ITEM:")
        rich.print(item)
        print()
        if item.name == "foo":
            raise HTTPException(status_code=400, detail="Item name cannot be foo.")
        inventory.append(item)
        return ResponseModel(ans="1", ans_1="2")

    # how to generate doc?
    # visit: http://<host_ip>:9981/docs
    #
    # how to export doc?
    #
    # By default, the OpenAPI schema is served at /openapi.json
    # this json file is needed to create project in apifox.
    # what is that json anyway?

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)
