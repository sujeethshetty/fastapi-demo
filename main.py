from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import convert, predict

app = FastAPI()

class StockIn(BaseModel):
    ticker: str

class StockOut(BaseModel):
    forecast: str


class Item(BaseModel):
    name: str
    description: str | None
    price: float
    tax: float | None


@app.get("/ping")
async def pong():
    return {"ping":"pong!"}

@app.post("/predict", response_model=StockOut, status_code=200)
async def get_prediction(payload: StockIn):
    ticker = payload.ticker
    prediction_list = predict(ticker)

    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model Not Found")
    response_obj = {"ticker": ticker, "forecast": str(convert(prediction_list))}
    return response_obj

@app.get("/")
async def read_root():
    return {"hello":"world"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q:Union[str, None]=None):
    return {"item_id":item_id, "q":q}

@app.post("/items/{item_id}")
def update_item(item_id:int, item:Item):
    return {"item_name": item.name, "item_id":item_id}

@app.post("/items/")
async def create_item(item:Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    return item_dict