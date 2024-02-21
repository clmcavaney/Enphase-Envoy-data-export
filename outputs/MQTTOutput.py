##
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <t3kpunk@gmail.com> wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Widmar 
# ----------------------------------------------------------------------------
# Heavily updated by Christopher McAvaney <christopher.mcavaney@gmail.com>
# Now uses the Homie Convention library (https://github.com/mjcumming/homie4) with 
# a locally defined "Solar Inverter Device".
##

import PluginLoader

from enphase_envoy_homie import Device_Enphase_Envoy
import time

class MQTTOutput(PluginLoader.Plugin):

    def __init__(self):
        # Translate config items to what homie mqtt library expects for mqtt settings
        mqtt_settings = {
            'MQTT_BROKER' : self.config.get('mqtt', 'host'),
            'MQTT_PORT' : int(self.config.get('mqtt', 'port')),
            'MQTT_USERNAME' : self.config.get('mqtt', 'user'),
            'MQTT_PASSWORD' : self.config.get('mqtt', 'passwd'),
        }

        self.logger.info('{}: creating Device_Solar_Inverter() homie instance'.format(self.__class__.__name__))
        self.enphase_envoy_device = Device_Enphase_Envoy( device_id=self.config.get('mqtt', 'device_id'), name=self.config.get('mqtt', 'name'), mqtt_settings=mqtt_settings )
        # being nice
        time.sleep(0.5)

    def process_message(self, msg):
        self.logger.debug('process_message(): publishing')

        self.enphase_envoy_device.update_details(msg.serial_number, msg.output_date, msg.output_time)
        self.enphase_envoy_device.update_production(msg.p_e_whToday, msg.p_e_whLifetime, msg.p_p_wNow, msg.p_v_rms, msg.p_pwr_f)
        self.enphase_envoy_device.update_consumption(msg.c_e_whToday, msg.c_e_whLifetime, msg.c_p_wNow, msg.c_v_rms, msg.c_pwr_f)

        # being nice
        time.sleep(0.5)

# vim:expandtab
# END OF FILE
