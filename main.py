from fastapi import FastAPI
import os
from fastapi.responses import PlainTextResponse
import send_telegram
import time
from playwright.sync_api import sync_playwright, TimeoutError
from jproperties import Properties
import give_kudos



app = FastAPI()

expected_token = 'eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJEYW5pZWwgTGFyYSIsIlVzZXJuYW1lIjoiVGFpa3VuIiwiZXhwIjoxNjcwMjY3NzkwLCJpYXQiOjE2NzAyNjc3OTB9.UIBkMMBkQ6OJgbt-QFASxVVlBG9MpPLJ7Br0YOOJEf0'


@app.get("/")
def root():
    send_telegram.send_to_telegram('Welcome')
    print('Welcome')
    return {"message": "Welcome to Give Kudos Utility"}


@app.get("/strava-kudos/{token}", response_class=PlainTextResponse)
def kudos(token: str):
    
    if token == expected_token:
        print('giving kudos')
        send_telegram.send_to_telegram('Trying to give kudos')
        kg = give_kudos.KudosGiver()
        kg.email_login()
        kg.give_kudos()
    else:
        print('Missing token')
    return {"Give kudos done sucessfully"}