import os
import shutil
import time

from lib.currency_datatypes import Reply
from lib.currency.utils import data, classified_data


class Mt5Client:
    def __init__(self, config):
        self.config = config
        self.files_path = config['common']['mql_files_path']

    def send_command(self, cmd, currencies):
        cmd_id = time.time()
        cmd_file = os.path.join(self.files_path, 'cmd_{}_{}'.format(cmd, cmd_id))
        with open(cmd_file, 'w') as c:
            c.write(currencies)
            c.flush()
        return cmd_id

    def wait_for_resp(self, cmd, cmd_id):
        retries = 10
        resp = os.path.join(self.files_path, 'resp_cmd_{}_{}'.format(cmd, cmd_id))
        while not os.path.exists(resp):
            retries -= 1
            time.sleep(0.4)
            if retries <= 0:
                return None
        return resp

    def rates(self, currencies, period=''):
        cmd_id = self.send_command('rates' + period, currencies)
        resp = self.wait_for_resp('rates', cmd_id)
        if not resp:
            return
        with open(resp) as stock_data:
            line = stock_data.readline().strip()
            if not line:
                return
            cur_stock, digits, price = line.split(',')
            rates = list()
            rates.append(float(price))
            while row := stock_data.readline():
                data = row.strip().split(',')
                if cur_stock != data[0]:
                    yield Reply(currency=cur_stock, digits=int(data[1]), rates=rates)
                    cur_stock, digits = data[0], int(data[1])
                    rates = list()
                rates.append(float(data[2]))
            yield Reply(currency=cur_stock, digits=int(digits), rates=rates)
        os.remove(resp)

    def rates_all(self, currencies, period):
        cmd_id = self.send_command('ratesall' + period, currencies)
        resp = self.wait_for_resp('ratesall' + period, cmd_id)
        if not resp:
            return
        with open(resp) as stock_data:
            line = stock_data.readline().strip()
            if not line:
                return
            cur_stock, digits, o_price, c_price, h_price, l_price = line.split(',')
            rates = list()
            rates.append([float(o_price), float(c_price), float(h_price), float(l_price)])
            while row := stock_data.readline():
                data = row.strip().split(',')
                if cur_stock != data[0]:
                    yield Reply(currency=cur_stock, digits=int(data[1]), rates=rates)
                    cur_stock, digits = data[0], int(data[1])
                    rates = list()
                rates.append([float(data[2]), float(data[3]), float(data[4]), float(data[5])])
            yield Reply(currency=cur_stock, digits=int(digits), rates=rates)
        os.remove(resp)

    def rates_all_stored(self, currencies, period, copy_to=None):
        cmd_id = self.send_command('ratesallstored' + period.lower(), currencies)
        resp_file_name = self.wait_for_resp('ratesallstored' + period.lower(), cmd_id)
        if copy_to:
            shutil.copyfile(resp_file_name, copy_to)
        return resp_file_name

    def chart(self, currency):
        cmd_id = self.send_command('chart', currency)
        resp = self.wait_for_resp('chart', cmd_id)
        os.remove(resp)
        # TODO. Add probably kind of notification to UI that chart was already displayed.

    @staticmethod
    def data(currency, filename=None):
        return data(currency, filename)

    @staticmethod
    def classified_data(currency, model_type='classified_data'):
        return classified_data(currency, model_type)
