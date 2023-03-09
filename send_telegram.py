import os

import requests
from jproperties import Properties
from dotenv import load_dotenv, find_dotenv

def send_to_telegram(message):

    TOKEN_ID = os.getenv('TOKEN_ID')
    CHAT_ID = os.getenv('CHAT_ID')

    apiURL = f"https://api.telegram.org/bot{TOKEN_ID}/sendMessage"

    try:
        response = requests.post(apiURL, json={"chat_id": CHAT_ID, "text": message})
        print(response.text)
    except Exception as e:
        print(e)
