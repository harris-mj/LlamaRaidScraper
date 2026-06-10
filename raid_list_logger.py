import requests
import os
from dotenv import load_dotenv
import json


load_dotenv()

API_KEY = os.getenv("BUNGIE_API_KEY")
MEMBERSHIP_TYPE = int(os.getenv("MEMBERSHIP_TYPE"))
MEMBERSHIP_ID = os.getenv("MEMBERSHIP_ID")
BASE_URL = "https://www.bungie.net/Platform"

HEADERS = {
    "X-API-Key": API_KEY
}

def get_characters():
    url = f"{BASE_URL}/Destiny2/{MEMBERSHIP_TYPE}/Profile/{MEMBERSHIP_ID}/?components=200"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    
    characters= data["Response"]["characters"]["data"]
    print(f"{len(characters)} characters found")
    return characters

def get_raids(char_id):
    all_activities =[]
    page = 0
    print(f"searching char {char_id} for raids")
    
    while True:
        print(f"Searching page {page}")
        url = f"{BASE_URL}/Destiny2/{MEMBERSHIP_TYPE}/Account/{MEMBERSHIP_ID}/Character/{char_id}/Stats/Activities/?mode=4&count=250&page={page}"
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        
        activities = data["Response"].get("activities") or []
        all_activities.extend(activities)
        print(f"{len(activities)} found")

        if len(activities) < 250 or len(activities) == 0:
            break

        page += 1

    return(all_activities)


def main():
    characters = get_characters()
    all_raids = []

    for char_id, char_data in characters.items():
        raids = get_raids(char_id)
        all_raids.extend(raids)
    
    outfile="data/raid_list.json"
    with open(outfile, "w") as f:
        json.dump(all_raids, f, indent=2)
        print(f"Saved activities to {outfile}")

if __name__ == "__main__":
    main()
