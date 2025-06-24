from fastapi import FastAPI
from enum import Enum

app = FastAPI(title="My First FastAPI App", version="1.0.0", description="This is my first FastAPI app")
@app.get("/")
async def ram():
    return {"message": "Hello World"}

@app.get("/items/{item_id:int}")
async def read_item(item_id):
    return {"items":item_id}

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

items = {"The Foo Wrestlers","Barz and the Bazz"}
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/itemsall/")
async def items_dist(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/items-query/{item_id}/user_id/{user_id}")
async def read_item(item_id: str, user_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item