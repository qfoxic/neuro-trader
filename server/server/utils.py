import os
import glob
from functools import cache
from corelib.utils import data, normalize_by_min_max


@cache
def load_trade_models(trade_op):
    return {
        os.path.basename(model): normalize_by_min_max(data(
            'empty', model)) for model in glob.glob(os.path.join('.', f'trademodels/{trade_op}/*'))
    }
