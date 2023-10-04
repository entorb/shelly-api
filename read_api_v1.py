"""
Access API gen1 of Shelly device (Plug S) using basic authentication.

see https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-settings
"""

import json

import requests

from credentials import password, shelly1_ip as shelly_ip, username

# public endpoint with no auth required
# url = f"http://{shelly_ip}/shelly"

# other endpoints require basic auth, if auth is configured in web interfaces
# status endpoint, shows much data, e.g. temperature
# see https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-meter-0
# url = f"http://{shelly1_ip}/status"

# read meter data
# see https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-status
url = f"http://{shelly_ip}/meter/0"

# creating session with http basic auth
session = requests.Session()
session.auth = (username, password)


# def write_data_to_file(data: dict) -> None:
#     with open("data.json", mode="w", encoding="utf-8", newline="\n") as fh:
#         json.dump(data, fh, ensure_ascii=False, sort_keys=False, indent=2)


try:
    response = session.get(url, timeout=3)

    if response.status_code == 200:
        # print(response.text)
        # convert response to dict
        data = json.loads(response.text)
        print(data)
        # write_data_to_file(data)

        # Current real AC power being drawn, in Watts
        watt_now = float(data["power"])
        # Total energy consumed by the attached electrical appliance in Watt-minute
        total = float(data["total"])
        # Energy counter value for the last 3 round minutes in Watt-minute
        watt_past_minutes = [float(x) for x in data["counters"]]
        # print(watt_past_minutes)
        # Timestamp of the last energy counter value, with the applied timezone
        timestamp = int(data["timestamp"])

    else:
        print(
            f"Failed to access the API. Status code: {response.status_code}, text: {response.text}",  # noqa: E501
        )

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {str(e)}")
