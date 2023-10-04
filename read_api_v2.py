"""
Access API v2 of Shelly device (Plus Plug S) using basic auth.

see https://shelly-api-docs.shelly.cloud/gen2/General/Authentication
"""

import requests

from credentials import shelly2_ip

# public endpoint with no auth required
# api_url = f"http://{shelly_ip}/shelly"

url = f"http://{shelly2_ip}/rpc"

data = {
    "id": 1,
    "method": "Shelly.GetStatus",
}


def extract_data_from_401(response_header: dict) -> dict[str, str | int]:
    """
    Extract data from Shelly 401 response and convert to dict.
    """
    data_out = {}
    s = response_header["WWW-Authenticate"]
    # remove " from values
    s = s.replace('"', "")
    # extract key-value pairs
    for key_value in s.split(", "):
        (key, value) = key_value.split("=")
        data_out[key] = value
    return data_out


try:
    response = requests.post(url, json=data, timeout=3)
    # 1. request without auth, get a onetime-no and http 401
    if response.status_code == 401:
        # print(response.headers)
        data = extract_data_from_401(response.headers)
        print(data)
        nonce = data["nonce"]
        realm = data["realm"]
    else:
        print(
            f"Failed to access the API. Status code: {response.status_code}, text: {response.text}",  # noqa: E501
        )

    # 2. request step 2 using SHA-256
    # TODO

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
