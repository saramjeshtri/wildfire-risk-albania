from dotenv import load_dotenv
import os
import requests

load_dotenv() # Loads variables from .env
firms_map_key = os.getenv("FIRMS_MAP_KEY") # Gets the value of FIRMS_MAP_KEY from .env

if not firms_map_key:
    raise ValueError("FIRMS_MAP_KEY not found — check your .env file")

response = requests.get("https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/{SOURCE}/{AREA_COORDINATES}/{DAY_RANGE}".format(
    MAP_KEY=firms_map_key,
    SOURCE="VIIRS_SNPP_NRT",
    AREA_COORDINATES="19.5,40.5,21.5,42.5",  # Example coordinates for Albania
    DAY_RANGE="4"
))

print(response.text)