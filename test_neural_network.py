from lib.config import ConfigReader
from lib.constants import CONFIG_FILENAME
from lib.currency_strategies import moving_average, get_price_percentage
from lib.mt5client import Mt5Client

config = ConfigReader(CONFIG_FILENAME).load()
client = Mt5Client(config)

SYMBOL = 'EURUSD'
reply = client.data(SYMBOL)

total = []
samples = []
X = []
y = []
max_len = 0
min_len = 99999
sample_types_map = {
    'sample_buy': 1,
    'sample_sell': 2,
    'sample_null': 3,
    'sample_almost_sell': 4,
    'sample_almost_buy': 5
}

for r in reply:
    if r.sample_type == 'total':
        total.append(r)
    else:
        max_len = max(len(r.data), max_len)
        min_len = min(len(r.data), min_len)
        samples.append(r)


print(f'MAX: {max_len}, MIN: {min_len}')
total = total[0]

for sample in samples:
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
    X.append(rec)
    y.append(sample_types_map[sample.sample_type])

# TODO. Take a look at the amount of test iris data.

#print(X)
#print(y)
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

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix


clf = MLPClassifier(solver='lbfgs', alpha=1e-5, shuffle=True, max_iter=3000,
                    hidden_layer_sizes=(30, 30, 30))

#scores = cross_validate(clf, X, y, cv=4,
#    scoring=('f1_weighted', 'accuracy', 'precision_weighted', 'recall_weighted'),
#    return_train_score=True
#)
#for i in scores:
#    if i.startswith('train_'):
#        print(i, scores[i])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf.fit(X, y)

predictions = clf.predict(X_train)
print(confusion_matrix(y_train,predictions))
print(classification_report(y_train,predictions))


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
