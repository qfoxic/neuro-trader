from lib.currency.indicators import moving_average, murray_levels, cos_similarity


class EnumeratedMovingAveragePricesStream:
    def __init__(self, sample, period):
        self.sample = sample
        self.candles_stream = self.sample.data
        self.period = period

    def __iter__(self):
        return enumerate(moving_average(
            self.sample,
            self.period,
            self.candles_stream[-1].time,
            self.candles_stream[0].time
        ))


class EnumeratedCosineSimilarityStream:
    def __init__(self, sample, model):
        self.sample = sample
        self.model = model

    def __iter__(self):
        return enumerate(cos_similarity(
            self.sample,
            self.model
        ))


class EnumeratedMurrayLevelsStream:
    def __init__(self, sample, period=200):
        self.sample = sample
        self.period = period

    def __iter__(self):
        return enumerate(murray_levels(
            self.sample,
            self.period
        ))


class EnumeratedCandlesStream:
    def __init__(self, sample):
        self.sample = sample

    def __iter__(self):
        return enumerate(self.sample.data)


class ReversedEnumeratedCandlesStream:
    def __init__(self, sample, from_pos=None):
        self.sample = sample
        self.from_pos = from_pos

    def __iter__(self):
        if self.from_pos:
            return enumerate(self.sample.data[self.from_pos::-1])
        return enumerate(self.sample.data[::-1])

