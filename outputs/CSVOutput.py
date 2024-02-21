import PluginLoader
from datetime import datetime

class CSVOutput(PluginLoader.Plugin):
    """Outputs the data to a file in CSV format"""

    def process_message(self, msg):
        """Process the message/data and output to file in CSV format.

        Args:
            msg (EnphaseEnvoy object): Contains what needs to be processed
        """
        with open(self.config.get('csv','filename'), 'a') as ofp:

            if not self.config.getboolean('csv', 'disable_header'):
                print('sn,date,time,p_e_whtoday,p_e_whlifetime,c_e_whtoday,c_e_whlifetime,p_wnow,p_v_rms,p_pwr_f,c_wnow,c_v_rms,c_pwr_f', file=ofp)

            print('{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(msg.serial_number, msg.output_date, msg.output_time, msg.p_e_whToday, msg.p_e_whLifetime, msg.c_e_whToday, msg.c_e_whLifetime, msg.p_p_wNow, msg.p_v_rms, msg.p_pwr_f, msg.c_p_wNow, msg.c_v_rms, msg.c_pwr_f), file=ofp)

# vim:expandtab
# END OF FILE
