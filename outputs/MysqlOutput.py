import PluginLoader
import datetime

class MysqlOutput(PluginLoader.Plugin):
    """Stores the data from the Omnik inverter into a mysql database"""

    def process_message(self, msg):
        """Store the information from the inverter in a MySQL database.

        Args:
            msg (EnphaseEnvoy object): Contains what needs to be processed
        """
        import pymysql
        import pymysql.err

        self.logger.debug('Connect to database')
        try:
            con = pymysql.connect(host=self.config.get('mysql', 'host'),
                                  user=self.config.get('mysql', 'user'),
                                  password=self.config.get('mysql', 'pass'),
                                  database=self.config.get('mysql', 'database'),
                                  cursorclass=pymysql.cursors.DictCursor)
        except pymysql.Error as e:
            print('error connecting to database')
            print('msg == {}: {}'.format(e.args[0], e.args[1]))
            return

        with con:
            with con.cursor() as cur:
                self.logger.debug('Executing SQL statement on database')
                sql = """INSERT INTO envoy_data
                        (sn, timestamp,
                        p_e_whToday, p_e_whLifetime, p_p_wnow, p_v_rms, p_pwr_f,
                        c_e_whToday, c_e_whLifetime, c_p_wnow, c_v_rms, c_pwr_f)
                        VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                timestamp = datetime.datetime.strptime(f'{msg.output_date} {msg.output_time}', "%Y%m%d %H:%M").strftime("%Y-%m-%d %H:%M:00")
                values = (msg.serial_number, timestamp,
                         msg.p_e_whToday, msg.p_e_whLifetime, msg.p_p_wNow, msg.p_v_rms, msg.p_pwr_f,
                         msg.c_e_whToday, msg.c_e_whLifetime, msg.c_p_wNow, msg.c_v_rms, msg.c_pwr_f)
                if self.config.getboolean('mysql', 'dry_run'):
                    self.logger.info('DRY RUN: cur.execute({}, ({}))'.format(sql, values))
                else:
                    self.logger.debug('cur.execute({}, ({}))'.format(sql, values))
                    try:
                        cur.execute(sql, values)

                        # autocommit isn't on by default
                        con.commit()    
                    except pymysql.err.DatabaseError as e:
                        print('MySQL error: {}'.format(e))
                        print('msg == {}'.format(msg))

# vim: expandtab
# END OF FILE
