from dotenv import load_dotenv
import os
import requests
import csv
import io
from db import get_connection

load_dotenv()
firms_map_key = os.getenv("FIRMS_MAP_KEY")

if not firms_map_key:
    raise ValueError("FIRMS_MAP_KEY not found — check your .env file")

url_template = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/{SOURCE}/{AREA_COORDINATES}/{DAY_RANGE}"
sources = ["VIIRS_SNPP_NRT", "VIIRS_NOAA20_NRT", "VIIRS_NOAA21_NRT"]


def fetch_all_fires():
    """Fetches fire detections from all VIIRS sources and returns a combined list."""
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
            row["source"] = source
            all_fires.append(row)
    return all_fires


def insert_fires(fires):
    """Inserts a list of fire records into the database."""
    conn = get_connection()
    cur = conn.cursor()
    for fire in fires:
        cur.execute(
            """
            INSERT INTO fires (latitude, longitude, bright_ti4, bright_ti5, scan, track, frp,
                                acq_date, acq_time, satellite, instrument, confidence, version, daynight, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (latitude, longitude, acq_date, acq_time, satellite) DO NOTHING
            """,
            (
                fire["latitude"], fire["longitude"], fire["bright_ti4"], fire["bright_ti5"],
                fire["scan"], fire["track"], fire["frp"], fire["acq_date"], fire["acq_time"],
                fire["satellite"], fire["instrument"], fire["confidence"], fire["version"],
                fire["daynight"], fire["source"]
            )
        )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {len(fires)} fire records into the database.")


if __name__ == "__main__":
    fires = fetch_all_fires()
    insert_fires(fires)