import sys
import os
from optparse import OptionParser

from corelib.utils import normalize_by_min_max, cos_similarity, data, make_sample, get_price_percentage


def pips2price(pips):
    # For most currencies
    return pips * 0.00001

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        start = i
        end = start + n
        yield lst[start: end]


def store_file(sample, title):
    with open(os.path.join('classified_patterns', f'{title}.txt'), 'a+') as f:
        for d in sample.data:
            row = '\t'.join(map(str, d))
            f.write(f'{row}\n')


def main(currency, model_size, precise):
    print(f'Loading total samples from data_{currency.upper()}')
    total_samples = data(currency, f'data_{currency.upper()}')

    for pattern_model in chunks(total_samples.data, model_size):
        sample = make_sample(pattern_model)
        firstCandle, lastCandle = sample.data[0], sample.data[-1]

        # Should be continuation sell pattern
        if firstCandle.open > lastCandle.open and firstCandle.close > lastCandle.close:
            # Let's measure "distance" between them
            firstIdx = get_price_percentage(firstCandle.close, sample.max_price, sample.min_price)
            lastIdx = get_price_percentage(lastCandle.close, sample.max_price, sample.min_price)
            if (firstIdx - lastIdx) > 50:
                normalized_model = normalize_by_min_max(sample)
                count = 0
                st_count = 0
                tp_count = 0
                for _sim, next_candles in cos_similarity(total_samples, normalized_model):
                    if (_sim > precise):
                        count += 1
                    # Let's check whether it was successful
                        takeprofit = lastCandle.close - pips2price(100)
                        stoploss = lastCandle.close + pips2price(100)
                        for cndl in next_candles:
                            if cndl.high >= stoploss:
                                st_count += 1
                                break
                            if cndl.low <= takeprofit:
                                tp_count += 1
                                break
                tp_percent = round((tp_count / count) * 100)
                st_percent = round((st_count / count) * 100)
                if count > 7 and tp_percent > 65:
                    store_file(sample.mirror(), f'{currency}_cont_sell_matches_{count}_st_{st_percent}_tp_{tp_percent}_mirror')
                    print(f"======== Continuation SELL model. Matches {count}. ST: {st_percent}, TP: {tp_percent} ========")
                    print(pattern_model)
            continue

        # Should be continuation buy pattern
        if firstCandle.open < lastCandle.open and firstCandle.close < lastCandle.close:
            # Let's measure "distance" between them
            firstIdx = get_price_percentage(firstCandle.close, sample.max_price, sample.min_price)
            lastIdx = get_price_percentage(lastCandle.close, sample.max_price, sample.min_price)
            if (firstIdx - lastIdx) > -50:
                normalized_model = normalize_by_min_max(sample)
                count = 0
                st_count = 0
                tp_count = 0
                for _sim, next_candles in cos_similarity(total_samples, normalized_model):
                    if (_sim > precise):
                        count += 1
                        # Let's check whether it was successful
                        takeprofit = lastCandle.close + pips2price(100)
                        stoploss = lastCandle.close - pips2price(100)
                        for cndl in next_candles:
                            if cndl.low <= stoploss:
                                st_count += 1
                                break
                            if cndl.high >= takeprofit:
                                tp_count += 1
                                break
                tp_percent = round((tp_count / count) * 100)
                st_percent = round((st_count / count) * 100)
                if count > 7 and tp_percent > 65:
                    store_file(sample, f'{currency}_cont_buy_matches_{count}_st_{st_percent}_tp_{tp_percent}')
                    print(f"======== Continuation BUY model. Matches {count}. ST: {st_percent}, TP: {tp_percent} ========")
                    print(pattern_model)
            continue

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-c', '--currency', dest='currency', default='eurusd')
    parser.add_option('-s', '--model-size', dest='model_size', default=30)
    parser.add_option('-p', '--precise', dest='precise', default=0.982)

    (options, args) = parser.parse_args()
    sys.exit(main(options.currency, options.model_size, options.precise))

#TODO. Store these patterns in a files within a folder