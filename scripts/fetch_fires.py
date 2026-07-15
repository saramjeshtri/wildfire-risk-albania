from dotenv import load_dotenv
import os
import requests
import csv
import io

load_dotenv()  # Loads variables from .env
firms_map_key = os.getenv("FIRMS_MAP_KEY")  # Gets the value of FIRMS_MAP_KEY from .env

if not firms_map_key:
    raise ValueError("FIRMS_MAP_KEY not found — check your .env file")

url_template = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/{SOURCE}/{AREA_COORDINATES}/{DAY_RANGE}"

sources = ["VIIRS_SNPP_NRT", "VIIRS_NOAA20_NRT", "VIIRS_NOAA21_NRT"]

all_fires = []

for source in sources:
    response = requests.get(url_template.format(
        MAP_KEY=firms_map_key,
        SOURCE=source,
        AREA_COORDINATES="19.3,39.6,21.1,42.7",
        DAY_RANGE="5"
    ))

    reader = csv.DictReader(io.StringIO(response.text))
    for row in reader:
        row["source"] = source  # tag which satellite this detection came from
        all_fires.append(row)

print(f"Total fire detections: {len(all_fires)}")
if all_fires:
    print(all_fires[0])