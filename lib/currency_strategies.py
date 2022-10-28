from collections import defaultdict
from datetime import datetime

import requests

from lib import constants as co
from lib.currency.utils import get_price_percentage, slope, price_delta

get_date = lambda: datetime.utcnow().strftime('%d-%m-%Y')

FINANCE_URL = (
    'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{}'
    '?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=US&'
    'modules=upgradeDowngradeHistory,recommendationTrend,'
    'financialData,earningsHistory,earningsTrend,industryTrend&'
    'corsDomain=currency.yahoo.com'
)


class InvalidPriceRange(BaseException):
    pass


class BaseStrategy:
    def __init__(self, currency, symbol_digits, rates, params=None):
        self.currency = currency
        self.symbol_digits = symbol_digits
        self.prices = rates
        self.params = params
        self.cur_price = self.prices[-1]
        self.max_price = max(self.prices)
        self.min_price = min(self.prices)

    def get_price_current_percentage(self, price):
        """Answers a question how close we are to the min in percents. Min == 0%, Max == 100%"""
        if self.max_price < self.min_price:
            raise InvalidPriceRange(f'{self.currency} max_price is less then min_price.\n'
                                    f'max_price = {self.max_price}\n'
                                    f'min_price = {self.min_price}\n')
        if not (self.min_price <= price <= self.max_price):
            raise InvalidPriceRange(
                f'{self.currency} cur_price is not within boundaries.\n'
                f'cur_price = {price}\n'
                f'max_price = {self.max_price}\n'
                f'min_price = {self.min_price}\n'
            )
        return get_price_percentage(price, self.max_price, self.min_price)

    def get_metrics(self):
        raise NotImplemented()


class SupportsStrategy(BaseStrategy):
    def __init__(self, currency, symbol_digits, rates, params):
        super(SupportsStrategy, self).__init__(currency, symbol_digits, rates)
        self.params = {
            'closest_support_threshold': (
                float(params.get('closest_support_threshold') or co.CLOSEST_SUPPORT_THRESHOLD)
            ),
            'slope_threshold': (
                float(params.get('slope_threshold') or co.SLOPE_THRESHOLD)
            )
        }
        self.supports = self.get_support_lines()

    def get_extrema_lines(self, sorted_rates):
        lines = defaultdict(int)
        x0, y0 = sorted_rates[0]
        # This is the lowest/highest point, so, should be included as support for sure.
        lines[y0] = co.SUPPORT_LINE_MAXIMUM_AMOUNT

        for x1, y1 in sorted_rates:
            sl = slope(x0, y0, x1, y1)
            if sl > self.params['slope_threshold']:
                x0, y0 = x1, y1
            lines[y0] += 1

        return [(p, a) for p, a in lines.items() if a > 1]

    def get_support_lines(self):
        supports_threshold = price_delta(self.max_price, self.min_price, self.symbol_digits) / 8.0
        sorted_rates_asc = sorted(self.prices)
        sorted_rates_desc = sorted(self.prices, reverse=True)
        sorted_norm_rates_asc = list(enumerate(sorted_rates_asc))
        sorted_norm_rates_desc = list(enumerate(sorted_rates_desc))
        filtered_minimas = sorted(
            self.get_extrema_lines(sorted_norm_rates_desc) + self.get_extrema_lines(sorted_norm_rates_asc))

        pivot_price = 0
        supports = {}
        avg_prices, avg_amounts = [], []

        for price, amount in filtered_minimas:
            if amount >= co.SUPPORT_LINE_MAXIMUM_AMOUNT:
                supports[round(price, self.symbol_digits)] = amount
            delta = price_delta(price, pivot_price, self.symbol_digits)
            avg_prices.append(price)
            avg_amounts.append(amount)
            if delta > supports_threshold:
                avg_price = sum(avg_prices) / len(avg_prices)
                avg_amount = sum(avg_amounts)
                supports[round(avg_price, self.symbol_digits)] = avg_amount
                pivot_price = price
                avg_prices, avg_amounts = [], []

        return supports

    def get_closest_support(self):
        for support in self.supports:
            if price_delta(self.cur_price, support, self.symbol_digits) <= self.params['closest_support_threshold']:
                return support
        return 0.00000

    def get_metrics(self):
        return {
            'percent_weight': str(round(self.get_price_current_percentage(self.cur_price), self.symbol_digits)),
            'closest_support': str(round(self.get_closest_support(), self.symbol_digits)),
            'closest_support_weight': str(self.supports.get(self.get_closest_support(), 0.00)),
            'supports': ','.join(map(str, self.supports))
        }


class DeepFallsStrategy(BaseStrategy):
    def get_falls(self):
        price_falls = []
        pivot_price = None

        for ind, cur_price in enumerate(self.prices):
            try:
                next_price = self.prices[ind + 1]
            except IndexError:
                break

            if cur_price >= next_price and pivot_price is None:
                pivot_price = cur_price
            if cur_price < next_price:
                if pivot_price:
                    diff = self.get_price_current_percentage(pivot_price) - self.get_price_current_percentage(
                        next_price)
                    price_falls.append(diff)
                pivot_price = None
        return price_falls

    def get_metrics(self):
        print(f'Currency {self.currency}')
        return {
            'price_fall_weight': str(round(self.get_falls()[-1], self.symbol_digits))
        }


class RecommendationRating(BaseStrategy):
    def get_mean_rec(self):
        r = requests.get(FINANCE_URL.format(self.currency))
        if not r.ok:
            return '-1'
        result = r.json()['quoteSummary']['result'][0]
        try:
            if not result['financialData']['recommendationMean']:
                return '-1'
            return result['financialData']['recommendationMean']['fmt']
        except KeyError:
            return '-1'

    def get_metrics(self):
        return {
            'rating': self.get_mean_rec()
        }


REGISTERED_STRATEGIES = {
    'SupportsStrategy': SupportsStrategy,
    'DeepFallsStrategy': DeepFallsStrategy,
    'RecommendationRating': RecommendationRating
}
