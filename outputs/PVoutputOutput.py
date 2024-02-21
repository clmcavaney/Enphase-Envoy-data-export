import PluginLoader
import datetime
import requests

class PVoutputOutput(PluginLoader.Plugin):
    """Sends the data to PVoutput.org"""

    def process_message(self, msg):
        """Process the message/data and send to PVoutput.org.

        Args:
            msg (EnphaseEnvoy object): Contains what needs to be processed

        """
        now = datetime.datetime.now()

        if (now.minute % 5) == 0 or self.config.getboolean('pvoutput', 'dry_run'):  # Only run at every 5 minute interval
            self.logger.debug('Uploading to PVoutput')

            url = "https://pvoutput.org/service/r2/addstatus.jsp"

            # always provided data
            get_data = {
                'key': self.config.get('pvoutput', 'apikey'),
                'sid': self.config.get('pvoutput', 'sysid'),
                'd': msg.output_date,
                't': msg.output_time,
                'v2': msg.p_p_wNow,
                'v4': msg.c_p_wNow,
                'v6': msg.p_v_rms
            }
            # optionally provided data
#            if self.config.getboolean('inverter', 'use_temperature'):
#                get_data['v5'] = msg.temperature
            if self.config.getboolean('pvoutput', 'provide_energy_value'):
                get_data['v1'] = msg.e_today * 1000

            self.logger.debug(get_data)
            if self.config.getboolean('pvoutput', 'dry_run'):
                self.logger.info('DRY RUN: request.get({}, params={})'.format(url, get_data))
                response = 'DRY RUN'
            else:
                response = requests.get(url, params=get_data)

            self.logger.debug('response: {}'.format(response))  # Log the response
            # allows the dry run case to be handled
            if hasattr(response, 'text'):
                self.logger.debug('response.text: {}'.format(response.text))  # Log the response
        else:
            self.logger.info('{}: not at a 5 minute interval'.format(__class__.__name__))

# vim:expandtab
# END OF FILE
