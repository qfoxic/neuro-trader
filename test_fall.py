from lib.config import ConfigReader
from lib.constants import CONFIG_FILENAME
from lib.mt5client import Mt5Client

config = ConfigReader(CONFIG_FILENAME).load()
client = Mt5Client(config)

SYMBOL = 'PLAY'
reply = list(client.rates(SYMBOL))[0]

prices = reply.rates
max_price = max(prices)
min_price = min(prices)


def get_price_current_percentage(cur_price):
    return ((cur_price - min_price) * 100) / (max_price - min_price)


pivot_price = None
fallbacks = []

for ind, cur_price in enumerate(prices):
    try:
        next_price = prices[ind + 1]
    except IndexError:
        break

    if cur_price >= next_price and pivot_price is None:
        pivot_price = cur_price
    if cur_price < next_price:
        if pivot_price:
            diff = get_price_current_percentage(pivot_price) - get_price_current_percentage(next_price)
            if diff >= 20.0:
                print(pivot_price, cur_price)
                fallbacks.append(diff)
        pivot_price = None

print(sorted(fallbacks))
