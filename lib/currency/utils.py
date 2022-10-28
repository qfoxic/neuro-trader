import os

from lib.constants import CLASSIFIED_SAMPLE_NAMES
from lib.currency_datatypes import Sample, Currency


def get_price_percentage(price, max_price, min_price):
    """Answers a question how close we are to the min in percents. Min == 0%, Max == 120%"""
    return ((price - min_price) * 120) / (max_price - min_price)


def get_murray_level(mrl, pivot_price):
    # mrl is a enumerated tuple (murray_level, price). Where murray level map is a following
    #   0: -2, 1: -1, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: +1, 12: +2
    murray_tuple_lower = None
    murray_tuple_higher = None

    for ind, price in mrl:
        murray_tuple_higher = ind, price
        if pivot_price > price:
            murray_tuple_lower = ind, price
        else:
            break

    if not (murray_tuple_higher and murray_tuple_lower):
        if not mrl:
            return 12
        return 0 if pivot_price < murray_tuple_higher[0] else 12

    # Kind of edge case, but sometimes the price can go above +2 level or below -2 level.
    # The price for lower and higher is equal. So, just return any tuple.
    if murray_tuple_higher[1] == murray_tuple_lower[1]:
        return murray_tuple_higher[0]

    price_position = get_price_percentage(pivot_price, murray_tuple_higher[1], murray_tuple_lower[1])
    if price_position <= 50:
        return murray_tuple_lower[0]
    return murray_tuple_higher[0]


def slope(x0, y0, x1, y1):
    if abs(x1 - x0) > 0:
        return abs(((y1 - y0) / (x1 - x0)) * 10000)
    return 0


def price_delta(p1, p2, symbol_digits):
    return abs(p1 - p2) * pow(10, symbol_digits - 1)


def classified_data(currency, model_type='classified_data'):
    currency = currency.upper()
    data_file = os.path.join('.', f'{model_type}_{currency}.txt')
    last_sample = None
    samples = []
    with open(data_file, 'r') as stock_data:
        for row in stock_data:
            row = row.strip().split(' ')[0]
            if not row:
                continue
            if row in CLASSIFIED_SAMPLE_NAMES:
                last_sample = Sample(currency=currency, sample_type=row.strip('##'))
                samples.append(last_sample)
                continue
            o_price, c_price, h_price, l_price, price_time = row.split(',')
            last_sample.data.append(
                Currency(
                    open=float(o_price),
                    close=float(c_price),
                    high=float(h_price),
                    low=float(l_price),
                    time=float(price_time)
                )
            )
        for sample in samples:
            sample.from_date = max(sample.data, key=lambda o: o.time).time
            sample.to_date = min(sample.data, key=lambda o: o.time).time
            sample.max_price = max(sample.data, key=lambda o: o.high).high
            sample.min_price = min(sample.data, key=lambda o: o.low).low
    return samples


def data(currency, filename=None):
    currency = currency.upper()
    data_file = os.path.join('.', filename or f'data_{currency}')
    sample = Sample(currency=currency, sample_type='total')
    with open(data_file, 'r') as stock_data:
        for row in stock_data:
            try:
                o_price, c_price, h_price, l_price, price_time = row.strip().split('\t')
                sample.data.append(
                    Currency(
                        open=float(o_price),
                        close=float(c_price),
                        high=float(h_price),
                        low=float(l_price),
                        time=float(price_time)
                    )
                )
            except ValueError as e:
                print(f'Error: {e}')

    sample.from_date = max(sample.data, key=lambda o: o.time).time
    sample.to_date = min(sample.data, key=lambda o: o.time).time
    sample.max_price = max(sample.data, key=lambda o: o.high).high
    sample.min_price = min(sample.data, key=lambda o: o.low).low
    return sample


def make_sample(currencies):
    sample = Sample(currency='', sample_type='')
    sample.from_date = max(currencies, key=lambda o: o.time).time
    sample.to_date = min(currencies, key=lambda o: o.time).time
    sample.max_price = max(currencies, key=lambda o: o.high).high
    sample.min_price = min(currencies, key=lambda o: o.low).low
    sample.data = currencies
    return sample


def normalize_by_min_max(sample):
    return [get_price_percentage(row.close, sample.max_price, sample.min_price) for row in sample.data]