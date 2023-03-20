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
    tags_metadata = [
        {
            "name": "users",
            "description": "Operations with users. The **login** logic is also here.",
            "externalDocs": {
                "description": "Items external docs",
                "url": "https://fastapi.tiangolo.com/",
            },
        },
        {
            "name": "items",
            "description": "Manage items. So _fancy_ they have their own docs.",
            "externalDocs": {
                "description": "Items external docs",
                "url": "https://fastapi.tiangolo.com/",
            },
        },
    ]

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
        tags_metadata=tags_metadata,
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

    from fastapi import Query

    @app.get(
        "/items/",
        response_description="get response example",
        summary="summary for get items",
        tags=["users"],  # this gets it into a folder.
    )  # what is dependencies anyway?
    async def read_items(
        q: int = Query(
            description="magic query number",
            default=42,
            examples=dict(
                e1=dict(summary="sum e1", description="desc e1", value=12),
                e2=dict(summary="sum e2", description="desc e2", value=23),
                e3=dict(summary="sum e3", description="desc e3", value=34),
            ),
        )
    ):
        print("MAGIC NUMBER?", q)
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
        is_offer: bool = Field(description='is')
        myDict: Mapping  # it is mapping, not dict.
        # if it is clear, you don't have to do this. if unclear, you do something different.

    inventory = []

    from pydantic import Field

    class ResponseModel(BaseModel):
        """model summary or description? example response model"""

        ans: str = Field(description="pydantic description", example="ans example")
        """ans doc"""
        ans_1: str

        class Config:
            schema_extra = {"example": {"ans": "Foo", "ans_1": "ans_1 data"}}

    from typing_extensions import Annotated  # python 3.7
    from fastapi import Body

    # when it is async, no parallelism!
    # but who needs that?
    @app.post(
        "/items/",
        description="api for creating an item",
        summary="summary for creating an item",
        response_description="respond if creation is successful.",
        response_model=Annotated[  # can this work?
            ResponseModel,
            Body(
                description="create item response model",
                examples={"normal": {"ans": "ans data", "ans_1": "ans_1 data"}},
            ),
        ],
        name="post_item_api_name",
    )
    async def create_item(
        item: Annotated[
            Item,
            Body(
                description="create item input param item",
                example=Item(name="name", price=2, is_offer=False, myDict={"m": 1}),
            ),
        ]
    ):
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
