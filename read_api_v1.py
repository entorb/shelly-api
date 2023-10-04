"""
Access API v1 of Shelly device (Plug S) using basic auth.

see https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-settings
"""

import json

import requests

from credentials import password, shelly1_ip, username

# public endpoint with no auth required
# url = f"http://{shelly_ip}/shelly"

# other endpoints require basic auth, if auth is configured in web interfaces
# status endpoint, shows much data
# see https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-meter-0
# url = f"http://{shelly1_ip}/status"
# read meter data
# see https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-meter-0
url = f"http://{shelly1_ip}/meter/0"


# creating session with http basic auth
session = requests.Session()
session.auth = (username, password)


def write_data_to_file(data: dict) -> None:
    with open("data.json", mode="w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, sort_keys=False, indent=2)


try:
    response = session.get(url, timeout=3)

    if response.status_code == 200:
        # print("API Response:")
        # print(response.text)
        # convert response to dict
        data = json.loads(response.text)
        # print(data)
        # write_data_to_file(data)
        watt_now = float(data["power"])
        kWh_total = float(data["total"])
        watt_past_minutes = [float(x) for x in data["counters"]]
        # list of 1-min power averages for last 3 minutes
    else:
        print(f"Failed to access the API. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {str(e)}")
