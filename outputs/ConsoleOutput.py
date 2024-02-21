import PluginLoader

# essentially a utility function - should probably be elsewhere
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


class ConsoleOutput(PluginLoader.Plugin):
    """Outputs the data from the Omnik inverter to stdout"""

    def process_message(self, msg):
        """Output the information from the inverter to stdout.

        Args:
            msg (EnphaseEnvoy object): Contains what needs to be processed
        """
        print("Serial Number: {0}".format(msg.serial_number))

        print("Date: {} Time: {}".format(msg.output_date, msg.output_time))
        print(" Production E Today: {0:>10} {1:>7}Wh  Lifetime: {2:<10} {3:>}Wh".format(msg.p_e_whToday, human_format(msg.p_e_whToday), msg.p_e_whLifetime, human_format(msg.p_e_whLifetime)))
        print("Consumption E Today: {0:>10} {1:>7}Wh  Lifetime: {2:<10} {3:>}Wh".format(msg.c_e_whToday, human_format(msg.c_e_whToday), msg.c_e_whLifetime, human_format(msg.c_e_whLifetime)))

        print(" Production Now: P: {0:>8} {1:>6}W V: {2:>7} F: {3:>4}".format(msg.p_p_wNow, human_format(msg.p_p_wNow), msg.p_v_rms, msg.p_pwr_f))
        print("Consumption Now: P: {0:>8} {1:>6}W V: {2:>7} F: {3:>4}".format(msg.c_p_wNow, human_format(msg.c_p_wNow), msg.c_v_rms, msg.c_pwr_f))

""" below is not Enphase previous Inverter data

        print("E Today: {0:>5}   Total: {1:<5}".format(msg.e_today, msg.e_total))
        print("H Total: {0:>5}   Temp:  {1:<5}"\
            .format(msg.h_total, msg.temperature))

        print("PV1   V: {0:>5}   I: {1:>4}".format(msg.v_pv(1), msg.i_pv(1)))
        print("PV2   V: {0:>5}   I: {1:>4}".format(msg.v_pv(2), msg.i_pv(2)))
        print("PV3   V: {0:>5}   I: {1:>4}".format(msg.v_pv(3), msg.i_pv(3)))

        print("L1    P: {0:>5}   V: {1:>5}   I: {2:>4}   F: {3:>5}"\
            .format(msg.p_ac(1), msg.v_ac(1), msg.i_ac(1), msg.f_ac(1)))
        print("L2    P: {0:>5}   V: {1:>5}   I: {2:>4}   F: {3:>5}"\
            .format(msg.p_ac(2), msg.v_ac(2), msg.i_ac(2), msg.f_ac(2)))
        print("L3    P: {0:>5}   V: {1:>5}   I: {2:>4}   F: {3:>5}"\
            .format(msg.p_ac(3), msg.v_ac(3), msg.i_ac(3), msg.f_ac(3)))
"""

# vim:expandtab
# END OF FILE
