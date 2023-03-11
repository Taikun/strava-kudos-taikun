import traceback
from datetime import datetime
import os

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse
from jproperties import Properties
from pydantic import BaseModel

import send_telegram
from give_kudos import KudosGiver

from dotenv import load_dotenv, find_dotenv

app = FastAPI()

load_dotenv(find_dotenv())

EXPECTED_TOKEN = os.getenv('TOKEN')

class Item(BaseModel):
    title: str
    token: str
    timestamp: datetime

@app.get("/healthcheck")
def read_root():
    return {"status": "ok"}


@app.get("/")
def root():
    send_telegram.send_to_telegram("Welcome")
    print("Welcome")
    return {"message": "Welcome to Give Kudos Utility, v1"}


@app.get("/strava-kudos/{token}", response_class=PlainTextResponse)
def kudos(token: str):
    # current date and time
    now = datetime.now()
    item = Item(title="Kudos giving started", token=token, timestamp=datetime.timestamp(now))
    json_compatible_item_data = jsonable_encoder(item)

    if token == EXPECTED_TOKEN:
        try:
            item = Item(title="Giving Kudos", token=token, timestamp=datetime.timestamp(now))
            print("giving kudos")
            kg = KudosGiver()
            kg.email_login()
            kg.give_kudos()
            kg.__del__()
            del kg
            item = Item(title="Gived Kudos", token=token, timestamp=datetime.timestamp(now))
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            print("Exception thrown, claro, algo pasa")  #
    else:
        print("Missing token")
        item = Item(title="Unexpcted token", token=token, timestamp=datetime.timestamp(now))
    return JSONResponse(content=json_compatible_item_data)


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8080)
