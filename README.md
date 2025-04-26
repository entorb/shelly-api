# shelly-api

Example Python (3.13) code for accessing the API of (password-protected) Shelly devices.

Written for Shelly Plug S and Plus Plug S according to [API gen1 spec](https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-meter-0) and [API gen2 spec](https://shelly-api-docs.shelly.cloud/gen2/General/Authentication).

Motivation: Shelly Plug S does not support local MQTT connection in parallel to cloud connection. Hence, I needed to retrieve the data (for my local InfluxDB and Grafana) via API instead.

Note: Password protection/authentication is activated in my devices, hence needed here as well.

* `credentials.py` set Shelly IP and login credentials
* `read_api_v1.py` example code for Shelly Plug S using API gen1
* `read_api_v2.py` example code for Shelly Plus Plug S using API gen2

## Features

* [x] access Shelly Plug S API gen1 via basic authentication
* [x] access Shelly Plus Plug S API gen2 via digest authentication / [RFC7616](https://datatracker.ietf.org/doc/html/rfc7616)
* [x] read meter power and energy data
