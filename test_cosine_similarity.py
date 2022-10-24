from lib.mt5client import Mt5Client
from lib.currency.utils import (data, normalize_by_min_max)
from lib.currency.indicators import cos_similarity
from lib.config import ConfigReader
from lib.constants import CONFIG_FILENAME


SYMBOL = 'EURUSD'
WINDOW = 300

config = ConfigReader(CONFIG_FILENAME).load()
client = Mt5Client(config)

total_samples = client.data(SYMBOL)

model = normalize_by_min_max(data(SYMBOL, f'classified_figure_{SYMBOL}.txt'))
cos_sim_stream = enumerate(cos_similarity(total_samples, model))

for ind, sim in cos_sim_stream:
    if sim > 0.985:
        print(ind, sim)

