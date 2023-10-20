import os
import time
from .datatypes import Sample, Currency


def normalize_by_min_max(sample):
    return [get_price_percentage(row.close, sample.max_price, sample.min_price) for row in sample.data]


def get_price_percentage(price, max_price, min_price):
    """Answers a question how close we are to the min in percents. Min == 0%, Max == 120%"""
    return ((price - min_price) * 120) / (max_price - min_price)


def data(currency, filename=None):
    currency = currency.upper()
    data_file = os.path.join('.', filename or f'data_{currency}')
    sample = Sample(currency=currency, sample_type='total')

    if not os.path.exists(data_file):
        return

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


def make_sample_from_array(prices):
    sample = Sample(currency='', sample_type='from_array')
    sample.from_date = int(time.time())
    sample.to_date = int(time.time())
    sample.max_price = max(prices)
    sample.min_price = min(prices)
    sample.data = [Currency(price, price, price, price, int(time.time())) for price in prices]
    return sample


# def cos_similarity(sample, model):
#     data = sample.data
#     wnd = len(model)
#     for ind, val in enumerate(data):
#         chunk = normalize_by_min_max(make_sample(data[ind:ind+wnd]))
#         next_candles = data[ind+wnd:ind+wnd+30]
#         if len(chunk) != len(model):
#             break
#         yield (cosine_similarity(chunk, model), next_candles)


# def cos_similarity1(sample, model):
#     data = sample.data
#     wnd = len(model)
#     for ind, val in enumerate(data):
#         chunk = normalize_by_min_max(make_sample(data[ind:ind+wnd]))
#         if len(chunk) != len(model):
#             break
#         yield (val.time, cosine_similarity(chunk, model))
