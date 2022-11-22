import sys
from optparse import OptionParser

from corelib.utils import normalize_by_min_max, cos_similarity1, data


def main(currency):
    print(f'Loading total samples from data_{currency.upper()}')
    total_samples = data(currency, f'data_{currency.upper()}')

    debug_matched_figures = []
    model = normalize_by_min_max(data(currency, f'classified_figure_{currency.upper()}.txt'))
    print('Running matching algorithm')
    cos_sim_stream = cos_similarity1(total_samples, model)

    print('Collecting results')
    for date, sim in cos_sim_stream:
        if sim > 0.97:
            debug_matched_figures.append([date, sim])
    print('Please copy string below')
    print(','.join([str(i[0]) for i in debug_matched_figures]))


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-c', '--currency', dest='currency', default='eurusd')

    (options, args) = parser.parse_args()
    sys.exit(main(options.currency))
