import matplotlib.pyplot as plt

from lib.config import ConfigReader
from lib.constants import CONFIG_FILENAME
from lib.currency_strategies import SupportsStrategy
from lib.mt5client import Mt5Client

config = ConfigReader(CONFIG_FILENAME).load()
client = Mt5Client(config)

SYMBOL = 'TSLA'
reply = list(client.rates(SYMBOL))[0]

strategy = SupportsStrategy(reply.currency, reply.digits, reply.rates, {})

prices = reply.rates
norm_rates = list(enumerate(prices))
plt.plot(list(map(lambda x: x[0], norm_rates)), prices, 'ro-', label='price')

supports = strategy.get_support_lines()
max_price = max(supports.keys())
min_price = min(supports.keys())
cur_price = prices[-1]
price_current_percentage = strategy.get_metrics()['percent_weight']
closest_support = strategy.get_metrics()['closest_support']

print(supports.keys())
print(f'Max {max_price}.\n Min {min_price}.\n Cur {cur_price}.\n '
      f'Percent {price_current_percentage}.\n Closest support {closest_support}')

for i in supports:
    plt.plot([0, 600], [i, i], 'ro-', label='support x', color='green')

plt.show()
