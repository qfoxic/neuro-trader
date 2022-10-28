from PyQt5.QtCore import QThread

from lib.currency_datatypes import CurrencyData


class CurrenciesLoader(QThread):
    def __init__(self, *args, **kwargs):
        self.queue = kwargs.pop('queue')
        self.commands_queue = kwargs.pop('commands_queue')
        self.client = kwargs.pop('client')
        self.config = kwargs.pop('config')
        super(CurrenciesLoader, self).__init__(*args, **kwargs)

    def run(self):
        while len(cmd := self.commands_queue.get()):
            resp = getattr(self.client, cmd.command)(cmd.currencies)
            if resp is None:
                continue
            for row in resp:
                self.queue.put_nowait(
                    CurrencyData(cmd.tab_id, row.rates, row.currency, row.digits)
                )
