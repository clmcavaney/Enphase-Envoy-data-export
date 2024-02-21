#!/usr/bin/python3

"""live-stats

Get data from the Enphase Envoy and output to console. This is a small
utility program that just changes the config to output anything to console.
"""
from enphase_envoy_data_export import EnphaseEnvoyDataExport


if __name__ == "__main__":
    config_file = 'enphase-envoy.conf'
    enphase_envoy_data_export = EnphaseEnvoyDataExport(config_file)

    enphase_envoy_data_export.override_config('general', 'enabled_plugins', 'ConsoleOutput')
    enphase_envoy_data_export.override_config('log', 'type', 'console')
    enphase_envoy_data_export.override_config('log', 'level', 'debug')
    enphase_envoy_data_export.run()

# vim:expandtab
# END OF FILE
