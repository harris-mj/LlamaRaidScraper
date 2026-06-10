import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BUNGIE_API_KEY")
MEMBERSHIP_TYPE = int(os.getenv("MEMBERSHIP_TYPE"))
MEMBERSHIP_ID = os.getenv("MEMBERSHIP_ID")
BASE_URL = "https://www.bungie.net/Platform"

HEADERS = {
    "X-API-Key": API_KEY
}

MEMBERSHIP_TYPE = 1        # Xbox
MEMBERSHIP_ID = "4611686018433509321"

def get_characters():
    url = f"{BASE_URL}/Destiny2/{MEMBERSHIP_TYPE}/Profile/{MEMBERSHIP_ID}/?components=200"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    import json
    print(json.dumps(data, indent=2))

    characters = data["Response"]["characters"]["data"]
    for char_id, char_data in characters.items():
        print(f"Character ID: {char_id}, Class: {char_data['classType']}")

get_characters()
