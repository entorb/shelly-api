# shelly-api

Example Python code for accessing the API of (password-protected) Shelly devices

Written for Shelly Plug S and Plus Plug S according to [API gen1 spec](https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-meter-0) and [API gen2 spec](https://shelly-api-docs.shelly.cloud/gen2/General/Authentication).

Motivation: Shelly Plug S does not support local MQTT connection in parallel to cloud connection. Hence, I needed to retrieve the data (for my local InfluxDB and Grafana) via API instead.

Note: Password protection/authentication is activated in my devices, hence needed here as well.

* `credentials.py` set Shelly IP and login credentials
* `read_api_v1.py` example code for Shelly API v1 (Plug S)
* `read_api_v2.py` example code for Shelly API v2 (Plus Plug S)

## Features

* [x] Shelly API v1 with basic authentication
* [ ] Shelly API v2 with authentication
