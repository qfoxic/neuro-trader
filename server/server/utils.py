import os
import glob
from functools import cache
from corelib.utils import data, normalize_by_min_max


@cache
def load_trade_models(mirror=False):
    # By default we have to present only buy models
    return {
        os.path.basename(model): normalize_by_min_max(
            data('empty', model).mirror() if mirror else data('empty', model))
        for model in glob.glob(os.path.join('.', 'trademodels', '*'))
    }
