#!/usr/bin/env python3

import os
import sys
import configparser
import logging
import logging.config
import requests
from urllib3.exceptions import InsecureRequestWarning

from PluginLoader import Plugin

from enphase_envoy import EnphaseEnvoy

class EnphaseEnvoyDataExport(object):
    config = None
    logger = None
    debug = True

    def __init__(self, config_file):
        if os.path.isfile(config_file) is not True:
            print('config file "{}" not found'.format(config_file))
            sys.exit(1)
        else:
            self.config = configparser.ConfigParser()
            self.config.read(config_file)

    def run(self):
        self.build_logger(self.config)

        # prepare path for plugin loading
        sys.path.append(self.__expand_path('outputs'))

        Plugin.config = self.config
        Plugin.logger = self.logger

        enabled_plugins = self.config.get('general', 'enabled_plugins').split(',')
        for plugin_name in enabled_plugins:
            plugin_name = plugin_name.strip()
            self.logger.debug('Importing output plugin ' + plugin_name)
            __import__(plugin_name)

        # Get data from Envoy
        envoy_host = self.config.get("envoy", "host")
        envoy_serial_number = self.config.get("envoy", "serial_number")
        enlighten_username = self.config.get("enlighten", "username")
        enlighten_password = self.config.get("enlighten", "password")
        token_file = self.config.get("enlighten", "tokenfile")

        # This is mostly for the Enphase Envoy connections as it is using a self signed certificate
        # Thank you Stack Overflow: https://stackoverflow.com/a/32282390/13102734
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        ee = EnphaseEnvoy(self.logger, envoy_host, envoy_serial_number, enlighten_username, enlighten_password, token_file)
        self.logger.debug(ee)
        self.logger.debug(ee.__dict__)

        ee.getProductionData()
        self.logger.debug(ee)

        self.logger.info('ee.p_p_wNow == {}W ee.p_e_whToday == {}Wh ee.p_e_whLifetime == {}Wh\nee.c_p_wNow == {}W ee.c_e_whNow == {}Wh ee.c_e_whLifetime == {}Wh'.format(ee.p_p_wNow, ee.p_e_whToday, ee.p_e_whLifetime, ee.c_p_wNow, ee.c_e_whToday, ee.c_e_whLifetime))


        # At this point pass the EnphaseEnvoy object through to the plugin
        for plugin in Plugin.plugins:
            self.logger.info('Run plugin {}'.format(plugin.__class__.__name__))
            plugin.process_message(ee)

    def build_logger(self, config):
        log_levels = dict(debug=10, info=20, warning=30, error=40, critical=50)
        log_dict = {
            'version': 1,
            'formatters': {
                'f': {'format': '%(asctime)s %(levelname)s %(message)s'}
            },
            'handlers': {
                'none': {'class': 'logging.NullHandler'},
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'f'
                },
                'file': {
                    'class': 'logging.handlers.WatchedFileHandler',
                    'filename': self.__expand_path(config.get('log',
                                                              'filename')),
                    'formatter': 'f'},
            },
            'loggers': {
                'EnphaseEnvoyDataLogger': {
                    'handlers': config.get('log', 'type').split(','),
                    'level': log_levels[config.get('log', 'level')]
                }
            }
        }
        logging.config.dictConfig(log_dict)
        self.logger = logging.getLogger('EnphaseEnvoyDataLogger')

    @staticmethod
    def __expand_path(path):
        # Expand relative path to absolute path
        if os.path.isabs(path):
            return path
        else:
            return os.path.join(os.path.dirname(os.path.abspath(__file__)),path)

if __name__ == '__main__':
    config_file = 'enphase-envoy.conf'
    enphase_envoy_data_export = EnphaseEnvoyDataExport(config_file)
    enphase_envoy_data_export.run()

# vim:expandtab
# END OF FILE
