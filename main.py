from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
import send_telegram
from jproperties import Properties
import give_kudos
import uvicorn
import traceback
from pydantic import BaseModel 
from datetime import datetime


app = FastAPI()

configs = Properties()
with open('kudos.properties', 'rb') as config_file:
    configs.load(config_file)
EXPECTED_TOKEN=configs.get("TOKEN").data

class Item(BaseModel):
    title: str
    token: str
    timestamp: datetime

@app.get("/")
def root():
    send_telegram.send_to_telegram('Welcome')
    print('Welcome')
    return {"message": "Welcome to Give Kudos Utility"}


@app.get("/strava-kudos/{token}", response_class=PlainTextResponse)
def kudos(token: str):
    # current date and time
    now = datetime.now()
    item = Item(title = "Kudos giving ok", token = token, timestamp=datetime.timestamp(now))
    json_compatible_item_data = jsonable_encoder(item)
    
    if token == EXPECTED_TOKEN:
        try:
            print('giving kudos')
            kg = give_kudos.KudosGiver()
            kg.email_login()
            kg.give_kudos()
            kg.__del__()
            del kg
            #give_kudos.fromAPI()
            
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            print("Exception thrown, claro, algo pasa") #
    else:
        print('Missing token')
    return JSONResponse(content=json_compatible_item_data)

if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000)