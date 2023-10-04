"""
Access API gen2 of Shelly device (Plus Plug S) using digest auth.

see https://shelly-api-docs.shelly.cloud/gen2/General/Authentication
"""
# import time
import random
import json

import hashlib
import requests

from credentials import shelly2_ip as shelly_ip, username, password

# public endpoint with no auth required
# api_url = f"http://{shelly_ip}/shelly"

url = f"http://{shelly_ip}/rpc"
method = "Shelly.GetStatus"
method = "Switch.GetStatus"
method_arg = "id=0"

payload_401 = {
    "id": 1,
    "method": method,
}


def extract_data_from_401(response_header: dict) -> dict[str, str | int]:
    """
    Extract data from Shelly 401 response and convert to dict.
    """
    data_401 = {}
    s = response_header["WWW-Authenticate"]
    s = s.replace("Digest qop", "qop")
    # remove " from values
    s = s.replace('"', "")
    # extract key-value pairs
    for key_value in s.split(", "):
        (key, value) = key_value.split("=")
        data_401[key] = value
    return data_401


# 1. request without auth, get a onetime-no and http 401
try:
    response = requests.post(
        url,
        timeout=3,
        json=payload_401,
        # data=json.dumps(payload_401),
    )
    if response.status_code == 401:
        # print(response.headers)
        data_401 = extract_data_from_401(response.headers)
    else:
        print(
            f"Failed to access the API. Status code: {response.status_code}, text: {response.text}",  # noqa: E501
        )
        exit()
    # print(data_401)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {str(e)}")
    exit()
except Exception as e:
    print(f"An error occurred: {str(e)}")
    exit()


# 2. request step 2 using SHA-256
print("Start Step 2")
try:
    auth_parts = [username, data_401["realm"], password]
    # Concatenate the auth_parts with ':' and compute the SHA-256 hash
    ha1 = hashlib.sha256(":".join(auth_parts).encode()).hexdigest()
    ha2 = hashlib.sha256(b"dummy_method:dummy_uri").hexdigest()
    # print(ha1)
    # print(ha2)

    # cnonce = str(int(time.time()))
    cnonce = str(random.randint(1000000, 9999999))  # noqa: S311

    nc = "1"  # number, nonce counter (returned only through websocket channel).
    # It has value of 1 if it is not available in the response

    s = ":".join((ha1, data_401["nonce"], nc, cnonce, "auth", ha2))
    resp = hashlib.sha256(s.encode()).hexdigest()

    d = {
        "id": 1,
        "method": method,
        "params": {"id": 0},  # 0 = first switch/meter
        "auth": {
            "realm": data_401["realm"],
            "username": username,
            "nonce": data_401["nonce"],
            "cnonce": cnonce,
            "response": resp,
            "algorithm": "SHA-256",
        },
    }
    response = requests.post(f"http://{shelly_ip}/rpc", json=d, timeout=3)
    res = json.loads(response.text)

    if response.status_code == 200:
        data = json.loads(response.text)
        data = data["result"]
        print(data)

        # Last measured instantaneous active power (in Watts) delivered to the attached load   # noqa: E501
        watt_now = float(data["apower"])
        # Total energy consumed in Watt-hours
        kWh_total = float(data["aenergy"]["total"])
        # Energy consumption by minute (in Milliwatt-hours) for the last three minutes
        past_minutes = [float(x) for x in data["aenergy"]["by_minute"]]
        # Unix timestamp of the first second of the last minute
        timestamp = int(data["aenergy"]["minute_ts"])
        # Temperature in Celsius (null if temperature is out of the measurement range)
        temp = float(data["temperature"]["tC"])

    else:
        print(
            f"Failed to access the API. Status code: {response.status_code}, text: {response.text}",  # noqa: E501
        )
        exit()

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
