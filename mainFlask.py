from flask import Flask
import traceback
from datetime import datetime
from give_kudos import KudosGiver
from jproperties import Properties
from pydantic import BaseModel 

app = Flask(__name__)

configs = Properties()
with open('kudos.properties', 'rb') as config_file:
    configs.load(config_file)
EXPECTED_TOKEN=configs.get("TOKEN").data


class Item(BaseModel):
    title: str
    token: str
    timestamp: datetime

@app.route("/strava-kudos/<token>")
def kudos(token: str):
    # current date and time
    print("Entering kudos flask")
    now = datetime.now()
    item = Item(title = "Kudos giving ok", token = token, timestamp=datetime.timestamp(now))
 
    
    if token == EXPECTED_TOKEN:
        try:
            print('giving kudos')
            kg = KudosGiver()
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
    return "Kudos Giving done ;)"


@app.route('/')
def hello():
    return 'Hello, World!'


# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()