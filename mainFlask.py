import traceback
from datetime import datetime
import os

from flask import Flask
from jproperties import Properties
from pydantic import BaseModel

import send_telegram
from give_kudos import KudosGiver
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)


load_dotenv(find_dotenv())
EXPECTED_TOKEN = os.getenv('TOKEN')


class Item(BaseModel):
    title: str
    token: str
    timestamp: datetime


@app.route("/strava-kudos/<token>")
def kudos(token: str):
    # current date and time
    print("Entering kudos flask")
    now = datetime.now()
    item = Item(title="Kudos giving ok", token=token, timestamp=datetime.timestamp(now))

    if token == EXPECTED_TOKEN:
        try:
            print("giving kudos")
            send_telegram.send_to_telegram("Trying to give kudos")
            kg = KudosGiver()
            kg.email_login()
            kg.give_kudos()
            kg.__del__()
            del kg
            send_telegram.send_to_telegram("Kudos sent sucessfully")
            # give_kudos.fromAPI()

        except Exception as e:
            print(traceback.format_exc())
            print(e)
            print("Exception thrown, claro, algo pasa")  #
    else:
        print("Missing token")
    return "Kudos Giving done ;)"


@app.route("/")
def hello():
    return "Hello, World!"


# main driver function
if __name__ == "__main__":

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
