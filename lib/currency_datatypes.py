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
    from_date: int = None
    to_date: int = None
    max_price: float = None
    min_price: float = None
    data: list = field(default_factory=list)


Currency = namedtuple('Currency', ['open', 'close', 'high', 'low', 'time'])
