import matplotlib.pyplot as plt
import shutil
import math

from lib.config import ConfigReader
from lib.constants import CONFIG_FILENAME
from lib.mt5client import Mt5Client

from lib.currency.utils import data
from lib.currency.indicators import murray_levels
from lib.workflows import MurrayLevelsSignal, MurrayLevelBuyFlowSmaller, MurrayLevelSellFlowSmaller

#config = ConfigReader(CONFIG_FILENAME).load()
#client = Mt5Client(config)
#shutil.move(client.rates_all_stored('EURUSD', 'h1'), './data_EURUSD')

total_samples = data('EURUSD')

samples = total_samples.data
print(len(samples))
prices = map(lambda x: x.close, samples)
sell = MurrayLevelsSignal(total_samples, MurrayLevelSellFlowSmaller, 10)
buy = MurrayLevelsSignal(total_samples, MurrayLevelBuyFlowSmaller, 3)

try:
    while buy.move():
        pass
except StopIteration:
    pass

#print('Buy signals')
#try:
#    while buy.move():
#        pass
#except StopIteration:
#    pass

#mml = murray_levels(total_samples, 200)
#plt.plot(list(prices), 'r-', label='price')
#last_m = []
#for ind, m in enumerate(mml):
    #if set(last_m) != set(m):
    #    print(ind, 'M CHANGED')
#    for i, p in m:
#        plt.plot([ind, ind + 1], [p, p], 'g-')
    #    last_m = m

#plt.show()
