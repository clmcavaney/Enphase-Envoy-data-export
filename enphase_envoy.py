#
# Class to handle the authenticaion and token process
# 

import sys
import os
import requests
import datetime
import jwt

# need to decide on where to save the token data - /tmp (i.e. empemerally) or a /var location (/var/cache or /home/<username>/var/cache)
# lets use data/token.txt and look to move it later

class EnphaseEnvoy:
    # TODO:
    # - setters
    # - getters

    # timeouts - dict where 'c' == connection timeout, and 'r' == read timeout
    def __init__(self, logger, envoy_host, envoy_serial_number, enlighten_username, enlighten_password, token_file, timeouts = {'c': 20, 'r': 15}):
        self.__logger = logger
        self.__envoy_host = envoy_host
        self.__envoy_serial_number = envoy_serial_number
        self.__enlighten_username = enlighten_username
        self.__enlighten_password = enlighten_password
        self.__token_file = token_file

        self.__connection_timeout = timeouts['c']
        self.__read_timeout = timeouts['r']
        self.__debug = True

        self.__enlighten_login_url = 'https://enlighten.enphaseenergy.com/login/login.json'

        self.__entrez_url = 'https://entrez.enphaseenergy.com/tokens'

        # where data is stored
        self._output_date = None
        self._output_time = None
        self._production_power_watt_now = None
        self._production_energy_watt_hr_today = None
        self._production_energy_watt_hr_lifetime = None
        self._consumption_power_watt_now = None
        self._consumption_energy_watt_hr_today = None
        self._consumption_energy_watt_hr_lifetime = None
        self._production_v_rms = None
        self._consumption_v_rms = None
        self._production_pwr_f = None
        self._consumption_pwr_f = None

        self.__token = None
        self.__obtain_token()


    @property
    def serial_number(self):
        return self.__envoy_serial_number

    @property
    def output_readingtime(self):
        return self._output_readingtime

    @property
    def output_date(self):
        return self._output_date

    @property
    def output_time(self):
        return self._output_time

    @property
    def p_p_wNow(self):
        return self._production_power_watt_now

    @property
    def p_e_whToday(self):
        return self._production_energy_watt_hr_today

    @property
    def p_e_whLifetime(self):
        return self._production_energy_watt_hr_lifetime

    @property
    def c_p_wNow(self):
        return self._consumption_power_watt_now

    @property
    def c_e_whToday(self):
        return self._consumption_energy_watt_hr_today

    @property
    def c_e_whLifetime(self):
        return self._consumption_energy_watt_hr_lifetime

    @property
    def p_v_rms(self):
        return self._production_v_rms

    @property
    def p_pwr_f(self):
        return self._production_pwr_f

    @property
    def c_v_rms(self):
        return self._consumption_v_rms

    @property
    def c_pwr_f(self):
        return self._consumption_pwr_f

    @property
    def debug(self):
        return self.__debug


    def __str__(self):
        p_p_kW = self._production_power_watt_now
        p_e_kWh_today = self._production_energy_watt_hr_today
        p_e_kWh_lifetime = self._production_energy_watt_hr_lifetime
        c_p_kW = self._consumption_power_watt_now
        c_e_kWh_today = self._consumption_energy_watt_hr_today
        c_e_kWh_lifetime = self._consumption_energy_watt_hr_lifetime
        if self._production_power_watt_now is not None:
            p_p_kW = float(format(self._production_power_watt_now / 1000, '.3f'))
        if self._production_energy_watt_hr_today is not None:
            p_e_kWh_today = float(format(self._production_energy_watt_hr_today / 1000, '.3f'))
        if self._production_energy_watt_hr_lifetime is not None:
            p_e_kWh_lifetime = float(format(self._production_energy_watt_hr_lifetime / 1000, '.3f'))
        if self._consumption_power_watt_now is not None:
            c_p_kW = float(format(self._consumption_power_watt_now / 1000, '.3f'))
        if self._consumption_energy_watt_hr_today is not None:
            c_e_kWh_today = float(format(self._consumption_energy_watt_hr_today / 1000, '.3f'))
        if self._consumption_energy_watt_hr_lifetime is not None:
            c_e_kWh_lifetime = float(format(self._consumption_energy_watt_hr_lifetime / 1000, '.3f'))
        return('{}: token: {}\nPower and Energy:\n  Production: {}W ({}kW) Today: {}Wh ({}kWh) Lifetime: {}Wh ({}kWh)\n  Consumption: {}W ({}kW) Today: {}Wh ({}kWh) Lifetime: {}Wh ({}kWh)\n  Production: {}V {}PF Consumption: {}V {}PF'.format(self.__class__.__name__, self.__token[0:15] + '...' + self.__token[-15:], self._production_power_watt_now, p_p_kW, self._production_energy_watt_hr_today, p_e_kWh_today, self._production_energy_watt_hr_lifetime, p_e_kWh_lifetime, self._consumption_power_watt_now, c_p_kW, self._consumption_energy_watt_hr_today, c_e_kWh_today, self._consumption_energy_watt_hr_lifetime, c_e_kWh_lifetime, self.p_v_rms, self.p_pwr_f, self.c_v_rms, self.c_pwr_f))


    def __obtain_token(self, refresh = False):
        # check for an existing token file
        if not os.path.exists(self.__token_file) or refresh is True:
            self.__logger.debug('{}: no token file found or refresh forced'.format(self.__class__.__name__))

            self.__token = self.__obtain_new_token()
        else:
            self.__logger.debug('{}: token file found, using that token'.format(self.__class__.__name__))
                
            # should really try to validate the contents before blindly reading in the token
            if os.stat(self.__token_file).st_size == 428:
                with open(self.__token_file, 'r') as ifp:
                    _token_encoded = ifp.read()

                try:
                    _token_decoded = jwt.decode(_token_encoded, algorithms=['ES256'], options={'verify_signature': False, 'verify_exp': True})
                except jwt.exceptions.DecodeError as error:
                    print('{}: token was unable to be decoded - {}'.format(self.__class__.__name__, error))
                    sys.exit(1)

                # check that the token hasn't expired
                needs_renewal = False
                try:
                    payload: dict[str, Any] = _token_decoded
                    exp: datetime = datetime.datetime.fromtimestamp(int(payload['exp']))
                    # if the expiry date is within 30 days, then renew the token
                    needs_renewal = datetime.datetime.now() > exp - datetime.timedelta(days=30)
                except jwt.exceptions.DecodeError as error:
                    print('{}: token was unable to be decoded - {}'.format(self.__class__.__name__, error))
                    sys.exit(1)

                if needs_renewal is True:
                    self.__token = self.__obtain_new_token()
                else:
                    self.__token = _token_encoded
            else:
                print('{}: token file doesn\'t look correct'.format(self.__class__.__name__))
                sys.exit(1)

        # Update the authorisation header with the new token
        self.__authorisation_header = {'Authorization': 'Bearer {}'.format(self.__token)}

    def __obtain_new_token(self):
        # login first
        data = {'user[email]': self.__enlighten_username, 'user[password]': self.__enlighten_password}
        self.__logger.debug('{}:__obtain_token(): data == {}'.format(self.__class__.__name__, data))
        self.__logger.debug('{}:__obtain_token(): url == {}'.format(self.__class__.__name__, self.__enlighten_login_url))
        try:
            resp = requests.post(self.__enlighten_login_url, data=data)
        except Exception as error:
            print('{}: request to Enphase Enlighten failed for login'.format(self.__class__.__name__))
            print('{}: error {}'.format(self.__class__.__name__, resp.text))
            print('{}: {} - {}'.format(type(error).__name__, error))
            sys.exit(1)

        self.__logger.debug('{}: response {}'.format(self.__class__.__name__, resp.text))
        resp_data = resp.json()

        self.__logger.debug('resp_data == {}'.format(resp_data))

        # get token second
        data = {'session_id': resp_data['session_id'], 'serial_num': self.__envoy_serial_number, 'username': self.__enlighten_username}
        self.__logger.debug('{}:__obtain_token(): data == {}'.format(self.__class__.__name__, data))
        try:
            resp = requests.post(self.__entrez_url, json=data)
        except Exception as error:
            print('{}: request to Entrez failed for token'.format(self.__class__.__name__))
            print('{}: {} - {}'.format(type(error).__name__, error))
            sys.exit(1)

        self.__logger.debug('resp.ok == {}'.format(resp.ok))
        self.__logger.debug('resp.status_code == {}'.format(resp.status_code))
        self.__logger.debug('token generated {}'.format(resp.text))

        # store the token in a file to use next time
        with open(self.__token_file, 'w') as ofp:
            ofp.write(resp.text)

        return resp.text

    def getProductionData(self):
        try:
            resp = requests.get(f'https://{self.__envoy_host}/production.json', timeout=(self.__connection_timeout, self.__read_timeout), verify=False, headers=self.__authorisation_header)
        except Exception as error:
            print('{}: request to Envoy failed for production data'.format(self.__class__.__name__))
            print('{}: {} - {}'.format(self.__class__.__name__, type(error).__name__, error))
            sys.exit(1)


        self.__logger.debug('resp == {}'.format(resp.json()))

        p_vrms = 0
        p_pwrf = 0
        PwhLifetime = PwhToday = PwNow = 0
        c_vrms = 0
        c_pwrf = 0
        CwhLifetime = CwhToday = CwNow = 0
        output_readingtime = 0
        # We are expecting a JSON response with production and consumption data
        for direction in ('production', 'consumption'):
            self.__logger.debug('direction: {}'.format(direction))
            # 0 == inverters
            # 1 == eim
            if direction == 'production':
                eim = resp.json()[direction][1]
                PwhLifetime = eim['whLifetime']
                PwhToday = eim['whToday']
                PwNow = 0 if eim['wNow'] < 0 else eim['wNow']
                p_vrms = eim['rmsVoltage']
                p_pwrf = eim['pwrFactor']
                output_readingtime = eim['readingTime']
            elif direction == 'consumption':
                eim = resp.json()[direction][0]
                CwhLifetime = eim['whLifetime']
                CwhToday = eim['whToday']
                CwNow = 0 if eim['wNow'] < 0 else eim['wNow']
                c_vrms = eim['rmsVoltage']
                c_pwrf = eim['pwrFactor']
            # this will be for production and consumption - purely for debugging below
            wNow = 0 if eim['wNow'] < 0 else eim['wNow']
            kwNow = float(format(wNow / 1000, '.3f'))
            whToday = eim['whToday']
            kwhToday = float(format(whToday / 1000, '.3f'))
            self.__logger.info('{}: {}({}) wNow {}W({}kW) whToday {}Wh({}kWh) {}Vrms [{}]'.format(direction, eim['readingTime'], datetime.datetime.fromtimestamp(eim['readingTime']), wNow, kwNow, whToday, kwhToday, eim['rmsVoltage'], eim['measurementType']))

        output_date = datetime.datetime.fromtimestamp(output_readingtime).strftime('%Y%m%d')
        output_time = datetime.datetime.fromtimestamp(output_readingtime).strftime('%H:%M')
        self.__logger.info('PVOutput Status: {} {} {} {} {} {} {}'.format(output_date, output_time, round(PwhToday), round(PwNow), round(CwhToday), round(CwNow), round(p_vrms, 2)))

        # store the data in the class variables
        self._output_readingtime = output_readingtime
        self._output_date = output_date
        self._output_time = output_time
        self._production_power_watt_now = PwNow
        self._production_energy_watt_hr_today = PwhToday
        self._production_energy_watt_hr_lifetime = PwhLifetime
        self._consumption_power_watt_now = CwNow
        self._consumption_energy_watt_hr_today = CwhToday
        self._consumption_energy_watt_hr_lifetime = CwhLifetime
        self._production_v_rms = p_vrms
        self._consumption_v_rms = c_vrms
        self._production_pwr_f = p_pwrf
        self._consumption_pwr_f = c_pwrf

# vim: expandtab
# END OF FILE
