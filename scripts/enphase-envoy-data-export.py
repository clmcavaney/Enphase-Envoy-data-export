#!/usr/bin/env python3

"""enphase-envoy-data-export

Get data from the Enphase Envoy and output as per config.
"""
from enphase_envoy_data_export import EnphaseEnvoyDataExport

if __name__ == "__main__":
    config_file = 'enphase-envoy.conf'
    enphase_envoy_data_export = EnphaseEnvoyDataExport(config_file)
    enphase_envoy_data_export.run()

# vim:expandtab
# END OF FILE
