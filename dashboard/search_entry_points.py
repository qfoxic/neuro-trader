import os
from optparse import OptionParser

from corelib.utils import normalize_by_min_max, cos_similarity1, data, mirror_normalized_array
from corelib.mt5client import Mt5Client
from dashboard.config import ConfigReader
from dashboard.constants import CONFIG_FILENAME


def check(currency, timeframe, precise, model_path):
    total_samples = data(currency, os.path.join('entries', f'sdata_{currency.upper()}_{timeframe.upper()}'))
    buy_model = normalize_by_min_max(data(currency, model_path))
    sell_model = mirror_normalized_array(buy_model)
    buy_cos_sim_stream = cos_similarity1(total_samples, buy_model)
    sell_cos_sim_stream = cos_similarity1(total_samples, sell_model)

    for _, sim in buy_cos_sim_stream:
        if sim > precise:
            print(f'DO BUY -> precise {sim}')
    for _, sim in sell_cos_sim_stream:
        if sim > precise:
            print(f'DO SELL -> precise {sim}')


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-p', '--precise', dest='precise', default=0.98, type=float)
    parser.add_option('-m', '--model', dest='model', default='classified_figure.txt', type=str)
    (options, args) = parser.parse_args()

    config = ConfigReader(CONFIG_FILENAME).load()
    client = Mt5Client(config)

    for currency in config['common']['currencies']:
        for timeframe in config['common']['timeframes']:
            client.srates_all_stored(currency, timeframe, os.path.join('entries', f'sdata_{currency.upper()}_{timeframe.upper()}'))
            print('==== Checking for entry points ', currency, timeframe, ' ===========')
            check(currency, timeframe, options.precise, options.model)
