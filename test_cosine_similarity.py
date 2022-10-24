from lib.config import ConfigReader
from lib.constants import CONFIG_FILENAME
from lib.currency.utils import get_price_percentage
from lib.currency.indicators import moving_average
from lib.mt5client import Mt5Client
from sklearn.model_selection import train_test_split
import random

import time
start = time.time()

config = ConfigReader(CONFIG_FILENAME).load()
client = Mt5Client(config)

SYMBOL = 'EURUSD'
total = client.data(SYMBOL)
samples = client.classified_data(SYMBOL)

train_samples = []
test_samples = []

X_train = []
y_train = []
X_test = []
y_test = []

sample_types_map = {
    'buy_0': 0,
    'buy_2': 2,
    'buy_3': 3,
    'sell_5': 5,
    'sell_7': 7
}

samples_by_type = {
    'buy_0': [],
    'buy_2': [],
    'buy_3': [],
    'sell_5': [],
    'sell_7': []
}


def get_sample_type(sample):
    sample_type = sample.sample_type
    if sample_type in ['buy_0', 'buy_1']:
        return 'buy_0'
    elif sample_type in ['buy_3', 'sell_4']:
        return 'buy_3'
    elif sample_type in ['sell_7', 'sell_6']:
        return 'sell_7'
    return sample_type


print('Split samples by type for further processing')
for sample in samples:
    samples_by_type[get_sample_type(sample)].append(sample)

print('Preparing train and test data')
for k in samples_by_type:
    print(f'Splitting {k}. Amount of data {len(samples_by_type[k])}')
    if k in ['buy_0', 'sell_7']:
        continue
    items = random.sample(samples_by_type[k], 2864)
    train_arr, test_arr = train_test_split(items, test_size=0.2)
    train_samples.extend(train_arr)
    test_samples.extend(test_arr)

print('Calculate MAs for train samples and prepare features and data')
for sample in train_samples:
    rec = []
    for ma_price in moving_average(total, 20, sample.from_date, sample.to_date):
        norm_ma_20 = get_price_percentage(ma_price, sample.max_price, sample.min_price)
        rec.append(norm_ma_20)
    for ma_price in moving_average(total, 50, sample.from_date, sample.to_date):
        norm_ma_50 = get_price_percentage(ma_price, sample.max_price, sample.min_price)
        rec.append(norm_ma_50)
    for currency in sample.data:
        norm_p = get_price_percentage(currency.close, sample.max_price, sample.min_price)
        rec.append(norm_p)
    X_train.append(rec)
    y_train.append(sample_types_map[get_sample_type(sample)])

print('Calculate MAs for test samples and prepare features and data')
for sample in test_samples:
    rec = []
    for ma_price in moving_average(total, 20, sample.from_date, sample.to_date):
        norm_ma_20 = get_price_percentage(ma_price, sample.max_price, sample.min_price)
        rec.append(norm_ma_20)
    for ma_price in moving_average(total, 50, sample.from_date, sample.to_date):
        norm_ma_50 = get_price_percentage(ma_price, sample.max_price, sample.min_price)
        rec.append(norm_ma_50)
    for currency in sample.data:
        norm_p = get_price_percentage(currency.close, sample.max_price, sample.min_price)
        rec.append(norm_p)
    X_test.append(rec)
    y_test.append(sample_types_map[get_sample_type(sample)])

print(time.time() - start)

# import matplotlib.pyplot as plt
#
# for i, p in enumerate(total.data):
#     norm_p = get_price_percentage(p.close, total.max_price, total.min_price)
#     plt.plot(i, norm_p, '.',  color='green')
#
# for i, ma_price in enumerate(moving_average(total, 20, total.from_date, total.to_date)):
#     norm_ma_20 = get_price_percentage(ma_price, total.max_price, total.min_price)
#     plt.plot(i, norm_ma_20, '.',  color='yellow')
#
# for i, ma_price in enumerate(moving_average(total, 50, total.from_date, total.to_date)):
#     norm_ma_50 = get_price_percentage(ma_price, total.max_price, total.min_price)
#     plt.plot(i, norm_ma_50, '.',  color='red')
#
# plt.show()

from sklearn.neural_network import MLPClassifier

from sklearn.metrics import classification_report,confusion_matrix


clf = MLPClassifier(
    activation='relu',
    solver='adam',
    learning_rate_init=0.00001,
    alpha=0.00001,
    batch_size=200,
    max_iter=5000,
    hidden_layer_sizes=(1000, 600),
    verbose=True
)
##### TODO.TODO.TODO. WE NEED MORE DATA

#mlp_gs = MLPClassifier(max_iter=4000)
#parameter_space = {
#    'hidden_layer_sizes': [(100, 100, 100),],
#    'activation': ['relu'],
#    'solver': ['adam',],
#    'alpha': [0.1, 0.01, 0.001, 0.0001, 0.00001],
#    'learning_rate_init': [0.01, 0.001, 0.0001, 0.00001, 0.000001]
#}
#from sklearn.model_selection import GridSearchCV
#clf = GridSearchCV(mlp_gs, parameter_space, n_jobs=-1, cv=5)
clf.fit(X_train, y_train)
#scores = cross_validate(clf, X, y, cv=4,
#    scoring=('f1_weighted', 'accuracy', 'precision_weighted', 'recall_weighted'),
#    return_train_score=True
#)
#for i in scores:
#    if i.startswith('train_'):
#        print(i, scores[i])

predictions = clf.predict(X_test)
print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))


# 1. Write a function to calc moving averages. DONE
# 2. Display them in a plot and verify with original. DONE
# 2.1 Display MAs on any sample and check it. DONE
# 3. Interpolate moving average into percent coordinate. Consider sample min and max. DONE
# 4. Display on a plot and verify with original. DONE

# 5. Prepare test data for neural network and train it on these moving averages. TODO
#     We need at least 50 examples of each sample.
#     Use GridSearchCV to get better parameters for neural network.
#             mlp_gs = MLPClassifier(max_iter=100)
#             parameter_space = {
#                 'hidden_layer_sizes': [(10,30,10),(20,)],
#                 'activation': ['tanh', 'relu'],
#                 'solver': ['sgd', 'adam'],
#                 'alpha': [0.0001, 0.05],
#                 'learning_rate': ['constant','adaptive'],
#             }
#             from sklearn.model_selection import GridSearchCV
#             clf = GridSearchCV(mlp_gs, parameter_space, n_jobs=-1, cv=5)
#             clf.fit(X, y)
#             print('Best parameters found:\n', clf.best_params_)
#     Calculate metrics: Accuracy , precision, recall,  f1-score,
#     Collect all data into list and prepare for neural network. We have to collect data for sell, buy and none
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
