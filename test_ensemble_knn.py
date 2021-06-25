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
    items = random.sample(samples_by_type[k], 603)
    # items = samples_by_type[k]
    train_arr, test_arr = train_test_split(items, test_size=0.1)
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
#    norm_p = get_price_percentage(p.close, total.max_price, total.min_price)
#    plt.plot(i, norm_p, '.',  color='green')
#
# for i, ma_price in enumerate(moving_average(total, 20, total.from_date, total.to_date)):
#    norm_ma_20 = get_price_percentage(ma_price, total.max_price, total.min_price)
#    plt.plot(i, norm_ma_20, '.',  color='yellow')
#
# for i, ma_price in enumerate(moving_average(total, 50, total.from_date, total.to_date)):
#    norm_ma_50 = get_price_percentage(ma_price, total.max_price, total.min_price)
#    plt.plot(i, norm_ma_50, '.',  color='red')
#
# plt.show()


from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.ensemble import BaggingClassifier

base_clf = KNeighborsClassifier(
    n_neighbors=10,
    algorithm='auto', #'auto', 'ball_tree', 'kd_tree', 'brute'
    weights='distance', # uniform,distance
    p=2,
    metric='minkowski' # 'mahalanobis', 'minkowski', 'seuclidean', 'wminkowski', 'euclidean', 'manhattan', chebyshev
)
clf = BaggingClassifier(base_clf, n_estimators=10, verbose=True, n_jobs=2)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))
