import sys
from optparse import OptionParser

from trader_corelib.utils import normalize_by_min_max, cos_similarity1, data, mirror_normalized_array


def main(currency):
    print(f'Loading total samples from data_{currency.upper()}')
    total_samples = data(currency, f'data_{currency.upper()}')

    buy_matched_figures = []
    sell_matched_figures = []

    buy_model = normalize_by_min_max(data(currency, f'classified_figure_{currency.upper()}.txt'))
    sell_model = mirror_normalized_array(buy_model)
    print('Running buy matching algorithm')
    buy_cos_sim_stream = cos_similarity1(total_samples, buy_model)
    print('Running sell matching algorithm')
    sell_cos_sim_stream = cos_similarity1(total_samples, sell_model)

    print('Collecting buy results')
    for date, sim in buy_cos_sim_stream:
        if sim > 0.98:
            buy_matched_figures.append([date, sim])
    print('Collecting sell results')
    for date, sim in sell_cos_sim_stream:
        if sim > 0.98:
            sell_matched_figures.append([date, sim])
    print('Buy:')
    print(','.join([str(i[0]) for i in buy_matched_figures]))
    print('Sell:')
    print(','.join([str(i[0]) for i in sell_matched_figures]))


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-c', '--currency', dest='currency', default='eurusd')

    (options, args) = parser.parse_args()
    sys.exit(main(options.currency))
