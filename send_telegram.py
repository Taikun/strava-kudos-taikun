import os

import requests
from jproperties import Properties


def send_to_telegram(message):

    configs = Properties()
    with open("kudos.properties", "rb") as config_file:
        configs.load(config_file)
    TOKEN_ID = configs.get("TOKEN_ID").data
    CHAT_ID = configs.get("CHAT_ID").data

    apiURL = f"https://api.telegram.org/bot{TOKEN_ID}/sendMessage"

    try:
        response = requests.post(apiURL, json={"chat_id": CHAT_ID, "text": message})
        print(response.text)
    except Exception as e:
        print(e)
