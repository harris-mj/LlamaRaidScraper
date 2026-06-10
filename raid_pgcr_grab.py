import requests
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()

API_KEY = os.getenv("BUNGIE_API_KEY")
MEMBERSHIP_TYPE = int(os.getenv("MEMBERSHIP_TYPE"))
MEMBERSHIP_ID = os.getenv("MEMBERSHIP_ID")
BASE_URL = "https://www.bungie.net/Platform"

HEADERS = {
    "X-API-Key": API_KEY
}

def de_dupe_raids():
    raid_list = "data/raid_list.json"
    with open(raid_list) as f:
        raids_full = json.load(f)
    print(f"{len(raids_full)} raids found")

    seen = set()
    unique = []
    for raid in raids_full:
        iid = raid["activityDetails"]["instanceId"]
        if iid not in seen:
            seen.add(iid)
            unique.append(raid)

    print(f"{len(unique)} unique raids found")
    
    return (unique)

def save_pgcr(instance_id):
    outfile = f"data/pgcr/{instance_id}.json"
    if os.path.exists(outfile):
        print(f"{outfile} already exists, skipping")
    else:
        url = f"https://www.bungie.net/Platform/Destiny2/Stats/PostGameCarnageReport/{instance_id}/"
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        with open(outfile,"w") as f:
              json.dump(data, f, indent=2)
        print(f"{outfile} written")
        time.sleep(0.5)






def main():
    os.makedirs("data/pgcr", exist_ok=True)
    raids = de_dupe_raids()
    
    for raid in raids:
        raid_iid = raid["activityDetails"]["instanceId"]
        save_pgcr(raid_iid)
    print("Saved all new raids")


if __name__ == "__main__":
    main()
