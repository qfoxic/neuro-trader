from collections import namedtuple
from dataclasses import dataclass, field
from itertools import tee

CurrencyData = namedtuple('CurrencyData', ['group', 'data', 'currency', 'symbol_digits'])
CurrencyProcessed = namedtuple('CurrencyProcessed', ['group', 'currency', 'metrics'])
Reply = namedtuple('Reply', ['currency', 'digits', 'rates'])
Command = namedtuple('Command', ['tab_id', 'command', 'currencies'])


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


@dataclass
class Sample:
    currency: str
    sample_type: str
    from_date: int = None
    to_date: int = None
    max_price: float = None
    min_price: float = None
    data: list = field(default_factory=list)

    def __len__(self):
        return len(self.data) - 1

    def mirror(self):
        math_matrics = [round(num[0].close - num[1].close, 4) for num in pairwise(self.data)]
        start_num = self.data[-1].close
        mirrored_data = []

        for ind, cur in enumerate(self.data):
            if ind == 0:
                mirrored_data.append(
                    Currency(open=cur.open, close=start_num, high=cur.high, low=cur.low, time=cur.time)
                )
                continue
            start_num = round(start_num + math_matrics[ind - 1], 4)
            mirrored_data.append(
                Currency(open=cur.open, close=start_num, high=cur.high, low=cur.low, time=cur.time)
            )
        self.data = mirrored_data
        return self

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
