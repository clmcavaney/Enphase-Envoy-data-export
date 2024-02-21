# Enphase-Envoy-data-export

A Python app to extract data from a local Enphase Envoy system and output that data to various different "outputs" (via a plugin mechanism).


## Description

A fork (or sorts) of Omnik-Data-Logger (https://github.com/clmcavaney/Omnik-Data-Logger.git) to get data from a local Enphase Envoy device and log it to one or more outputs.  This version has been created to get data from an Enphase Envoy instead of an Omniksol Solar inverter.

This includes production (aka generation) and consumption data.

Outputs can be:
- Console - directly to the CLI
- CSV - to a file in CSV format
- MQTT - to your MQTT broker/server following the Homie IoT Convention format
- MySQL - to your MySQL server
- PVOutput - to PVOutput station that you have configured

**Note:** The MQTT output requires an additional library (which has been included) called `enphase_envoy_homie`.  This is an implementation of MQTT Device under the Homie IoT convention (see https://homieiot.github.io/ for more details).


## Acknowledgements

Wouter (https://github.com/Woutrrr) for https://github.com/Woutrrr/Omnik-Data-Logger

Will Hart (https://gist.github.com/will-hart | https://willhart.io/) for the Python Plugin Class - https://gist.github.com/will-hart/5899567

Ian Mills (https://github.com/vk2him) for the Envoy login/token logic for the newer firmware of these devices - https://github.com/vk2him/Enphase-Envoy-mqtt-json

