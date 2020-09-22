from lib.config import ConfigReader
from lib.constants import CONFIG_FILENAME
from lib.mt5client import Mt5Client
from lib.currency_strategies import moving_average, get_price_percentage

config = ConfigReader(CONFIG_FILENAME).load()
client = Mt5Client(config)

SYMBOL = 'EURUSD'
reply = client.data(SYMBOL)

total = []
sample = []
for r in reply:
    if r.sample_type == 'total':
        total.append(r)
    else:
        sample.append(r)


#import matplotlib.pyplot as plt
#for i, p in enumerate(reversed(list(moving_average(total[0], 50, sample[0].from_date, sample[0].to_date)))):
#    norm_ma_50 = get_price_percentage(p, sample[0].max_price, sample[0].min_price)
#    plt.plot(i, norm_ma_50, '.',  color='red')

#for i, p in enumerate(reversed(list(moving_average(total[0], 20, sample[0].from_date, sample[0].to_date)))):
#    norm_ma_20 = get_price_percentage(p, sample[0].max_price, sample[0].min_price)
#    plt.plot(i, norm_ma_20, '.',  color='blue')

#for i, p in enumerate(reversed(sample[0].data)):
#    norm_p = get_price_percentage(p.close, sample[0].max_price, sample[0].min_price)
#    plt.plot(i, norm_p, '.',  color='green')

#plt.show()

from sklearn.neural_network import MLPClassifier
X = [[0., 0.], [1., 1.]]
y = [0, 1]
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 2), random_state=1)
clf.fit(X, y)
print(clf.predict([[2., 2.], [-1., -2.], [-1., -1.]]))


# 1. Write a function to calc moving averages. DONE
# 2. Display them in a plot and verify with original. DONE
# 2.1 Display MAs on any sample and check it. DONE
# 3. Interpolate moving average into percent coordinate. Consider sample min and max. DONE
# 4. Display on a plot and verify with original. DONE

# 5. Prepare test data for neural network and train it on these moving averages. TODO
#     Collect all data into list and prepare for neural network.
#     Train network.
#     Run different cross validation methods.


# 6. Collect samples from different currencies and verify neural network
# 7. Add smooth function to currency values and train neural network with these smooth
# values which should be translated to percents.




# Implement CCI indicator
# Implement murray levels indicator
# Implement method to simplify price data, based on a close price, should use only Y axis
# figure out few examples of a price condensation
# Build neural network on top of these figures. It should accept normalized prices with Y axis only.
