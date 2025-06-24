from fastapi import FastAPI,Query
from pydantic import BaseModel
from typing import Annotated

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


@app.put("/items-query/{item_id}")
async def update_item_query_param_annotate(item_id: int, item: Item, q: Annotated[str | None, Query(max_length=20) ]):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

