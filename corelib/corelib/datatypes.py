from collections import namedtuple
from dataclasses import dataclass, field

CurrencyData = namedtuple('CurrencyData', ['group', 'data', 'currency', 'symbol_digits'])
CurrencyProcessed = namedtuple('CurrencyProcessed', ['group', 'currency', 'metrics'])
Reply = namedtuple('Reply', ['currency', 'digits', 'rates'])
Command = namedtuple('Command', ['tab_id', 'command', 'currencies'])


@dataclass
class Sample:
    currency: str
    sample_type: str
    from_date: int | None = None
    to_date: int | None = None
    max_price: float | None = None
    min_price: float | None  = None
    data: list = field(default_factory=list)


@dataclass
class TradeInfo:
    currency: str
    spread: float
    time1: int
    forecast1: int
    actual1: int
    prev1: int
    impact1: int # 0 - no impact, 1 - positive, 2 - negative
    time2: int
    forecast2: int
    actual2: int
    prev2: int
    impact2: int # 0 - no impact, 1 - positive, 2 - negative
    news1_name: str
    news2_name: str

    def formatted_info(self):
        return {
            'spread': self.spread,
            self.currency[0:3]: {
                'time': self.time1, 'forecast': self.forecast1,
                'actual': self.actual1, 'prev': self.prev1, 'impact': self.impact1,
                'event': self.news1_name},
            self.currency[-3:]: {
                'time': self.time2, 'forecast': self.forecast2,
                'actual': self.actual2, 'prev': self.prev2, 'impact': self.impact2,
                'event': self.news2_name}
        }


Currency = namedtuple('Currency', ['open', 'close', 'high', 'low', 'time'])
