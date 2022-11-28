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
            print(f'{currency} {timeframe} BUY -> {sim}')
    for _, sim in sell_cos_sim_stream:
        if sim > precise:
            print(f'{currency} {timeframe} SELL -> {sim}')


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-p', '--precise', dest='precise', default=0.98, type=float)
    parser.add_option('-m', '--model', dest='model', default='classified_figure.txt', type=str)
    (options, args) = parser.parse_args()

    config = ConfigReader(CONFIG_FILENAME).load()
    client = Mt5Client(config)
    for currency in config['common']['currencies']:
        if not currency:
            break
        print(f'======== Verifying {currency}')
        trade_info = client.get_info(currency)
        if trade_info:
            info = trade_info.formatted_info()
            spread = info['spread']

            pair1_impact = 'no'
            pair2_impact = 'no'

            match info[currency[0:3]]['impact']:
                case 1:
                    pair1_impact = 'positive'
                case 2:
                    pair1_impact = 'negative'

            match info[currency[-3:]]['impact']:
                case 1:
                    pair2_impact = 'positive'
                case 2:
                    pair2_impact = 'negative'

            pair1_news_in = int((info[currency[0:3].upper()]["time"]) / 60)
            pair2_news_in = int((info[currency[-3:].upper()]["time"]) / 60)
            event1 = info[currency[0:3].upper()]["event"]
            event2 = info[currency[-3:].upper()]["event"]
            print(f'Spread {spread}')
            print(f'{currency[0:3].upper()} news {event1} in {pair1_news_in if pair1_news_in <= 30 else "N/A"} minutes, impact {pair1_impact}')
            print(f'{currency[-3:].upper()} news {event2} in {pair2_news_in if pair2_news_in <= 30 else "N/A"} minutes, impact {pair2_impact}')


        for timeframe in config['common']['timeframes']:
            if not timeframe:
                break
            client.srates_all_stored(currency, timeframe, os.path.join('entries', f'sdata_{currency.upper()}_{timeframe.upper()}'))
            check(currency, timeframe, options.precise, options.model)
