from fastapi import FastAPI
from give_kudos import KudosGiver
import send_telegram

app = FastAPI()

token = 'eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJEYW5pZWwgTGFyYSIsIlVzZXJuYW1lIjoiVGFpa3VuIiwiZXhwIjoxNjcwMjY3NzkwLCJpYXQiOjE2NzAyNjc3OTB9.UIBkMMBkQ6OJgbt-QFASxVVlBG9MpPLJ7Br0YOOJEf0'

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/strava-kudos/{token}")
async def kudos():
    print('giving kudos')

    kg = KudosGiver()
    kg.email_login()
    kg.give_kudos()
    
    return {"message": "Hello World"}