import sys
from optparse import OptionParser

from trader_corelib.mt5client import Mt5Client


def main(currency):
    print(f'Loading total samples from {currency.upper()}')
    client = Mt5Client({'common': {'mql_files_path': '/System/Volumes/Data/Users/volodymyrpaslavskyy/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5/MQL5/Files'}})
    client.rates_all_stored(currency, 'h4', f'./loaded_timeseries_{currency}')


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-c', '--currency', dest='currency', default='eurusd')

    (options, args) = parser.parse_args()
    sys.exit(main(options.currency))
