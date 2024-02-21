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


## Installation and Setup

1. Clone this repository
```
$ git clone https://github.com/clmcavaney/Enphase-Envoy-data-export.git
$ cd Enphase-Envoy-data-export
```

2. Copy the config example to `enphase-envoy.conf`
```
$ cp enphase-envoy-example.conf enphase-envoy.conf
```

3. Change the settings in `enphase-config.conf`

4. Test your settings with `scripts/live-stats.py`
If successful, you should see data from your Envoy
```
$ ./scripts/live-stats.py
```

5. Run the script with `scripts/enphase-envoy-data-extract.py`
```
$ ./scripts/enphase-envoy-data-extract.py
```


## Acknowledgements

Wouter (https://github.com/Woutrrr) for https://github.com/Woutrrr/Omnik-Data-Logger

Will Hart (https://gist.github.com/will-hart | https://willhart.io/) for the Python Plugin Class - https://gist.github.com/will-hart/5899567

Ian Mills (https://github.com/vk2him) for the Envoy login/token logic for the newer firmware of these devices - https://github.com/vk2him/Enphase-Envoy-mqtt-json

