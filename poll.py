import sys
from datetime import datetime, timezone

import requests

from config import DESTINATION, ORIGIN, TOMTOM_API_KEY
from db import init_db, insert_sample

ROUTING_URL = (
    "https://api.tomtom.com/routing/1/calculateRoute/"
    "{origin_lat},{origin_lon}:{dest_lat},{dest_lon}/json"
)


def fetch_travel_time():
    url = ROUTING_URL.format(
        origin_lat=ORIGIN[0],
        origin_lon=ORIGIN[1],
        dest_lat=DESTINATION[0],
        dest_lon=DESTINATION[1],
    )
    params = {
        "key": TOMTOM_API_KEY,
        "traffic": "true",
        "routeType": "fastest",
    }
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    summary = response.json()["routes"][0]["summary"]
    return {
        "travel_time_seconds": summary["travelTimeInSeconds"],
        "traffic_delay_seconds": summary.get("trafficDelayInSeconds", 0),
        "length_meters": summary["lengthInMeters"],
    }


def main():
    init_db()
    try:
        result = fetch_travel_time()
    except requests.RequestException as e:
        print(f"Failed to fetch travel time: {e}", file=sys.stderr)
        sys.exit(1)

    fetched_at = datetime.now(timezone.utc).isoformat()
    insert_sample(
        fetched_at,
        result["travel_time_seconds"],
        result["traffic_delay_seconds"],
        result["length_meters"],
    )
    minutes = result["travel_time_seconds"] / 60
    print(f"[{fetched_at}] travel time: {minutes:.1f} min "
          f"(delay: {result['traffic_delay_seconds'] / 60:.1f} min)")


if __name__ == "__main__":
    main()
