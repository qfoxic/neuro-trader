from PyQt5.QtCore import QThread, pyqtSignal

from lib.currency_datatypes import CurrencyProcessed
from lib.currency_strategies import REGISTERED_STRATEGIES


class StrategyNotFound(BaseException):
    pass


class CurrenciesProcessor(QThread):
    dataProcessed = pyqtSignal(CurrencyProcessed)

    def __init__(self, *args, **kwargs):
        self.queue = kwargs.pop('queue')
        self.config = kwargs.pop('config')

        super(CurrenciesProcessor, self).__init__(*args, **kwargs)

    def run(self):
        while len(currency_data := self.queue.get()):
            conf = self.config[currency_data.group]

            currency = currency_data.currency
            digits = currency_data.symbol_digits
            data = currency_data.data

            if currency_data.symbol_digits is None:
                print(f'No digits found for {currency}')
                continue
            if currency_data.data is None:
                print(f'No rates found for {currency}')
                continue

            strategies = conf['strategies']
            if isinstance(strategies, str):
                strategies = [strategies, ]
            metrics = {}
            for strategy in strategies:
                strat = REGISTERED_STRATEGIES.get(strategy)
                if not strat:
                    raise StrategyNotFound()
                metrics.update(strat(currency, digits, data, conf).get_metrics())

            self.dataProcessed.emit(CurrencyProcessed(
                group=currency_data.group,
                currency=currency,
                metrics=metrics
            ))
