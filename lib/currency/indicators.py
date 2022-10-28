import math
from sklearn.metrics.pairwise import cosine_similarity
from lib.currency.utils import normalize_by_min_max, make_sample


def _calc_murray_levels(samples):
    if not samples:
        return []
    v1 = min(samples, key=lambda x: x.low).low
    v2 = max(samples, key=lambda x: x.high).high
    fractal = 0

    if 250000 >= v2 > 25000:
        fractal = 100000
    elif 25000 >= v2 > 2500:
        fractal = 10000
    elif 2500 >= v2 > 250:
        fractal = 1000
    elif 250 >= v2 > 25:
        fractal = 100
    elif 25 >= v2 > 12.5:
        fractal = 12.5
    elif 12.5 >= v2 > 6.25:
        fractal = 12.5
    elif 6.25 >= v2 > 3.125:
        fractal = 6.25
    elif 3.125 >= v2 > 1.5625:
        fractal = 3.125
    elif 1.5625 >= v2 > 0.390625:
        fractal = 1.5625
    elif 0.390625 >= v2 > 0:
        fractal = 0.1953125

    price_range = v2 - v1
    summary = math.floor(
        math.log(fractal / price_range) / math.log(2)
    )
    octave = fractal * (pow(0.5, summary))
    mn = math.floor(v1 / octave) * octave
    mx = mn + octave if (mn + octave) > v2 else mn + (2 * octave)
    x2 = mn + (mx - mn) / 2 if ((v1 >= (3 * (mx - mn) / 16 + mn)) and (v2 <= (9 * (mx - mn) / 16 + mn))) else 0
    x1 = mn + (mx - mn) / 2 if ((v1 >= (mn - (mx - mn) / 8)) and (v2 <= (5 * (mx - mn) / 8 + mn)) and (x2 == 0)) else 0
    x4 = mn + 3 * (mx - mn) / 4 if ((v1 >= (mn + 7 * (mx - mn) / 16)) and (v2 <= (13 * (mx - mn) / 16 + mn))) else 0
    x5 = mx if ((v1 >= (mn + 3 * (mx - mn) / 8)) and (v2 <= (9 * (mx - mn) / 8 + mn)) and (x4 == 0)) else 0
    x3 = mn + 3 * (mx - mn) / 4 if (
            (v1 >= (mn + (mx - mn) / 8)) and (v2 <= (7 * (mx - mn) / 8 + mn)) and (x1 == 0) and (x2 == 0) and (
            x4 == 0) and (x5 == 0)) else 0
    x6 = mx if ((x1 + x2 + x3 + x4 + x5) == 0) else 0
    finalH = x1 + x2 + x3 + x4 + x5 + x6
    y1 = mn if x1 > 0 else 0
    y2 = mn + (mx - mn) / 4 if x2 > 0 else 0
    y3 = mn + (mx - mn) / 4 if x3 > 0 else 0
    y4 = mn + (mx - mn) / 2 if x4 > 0 else 0
    y5 = mn + (mx - mn) / 2 if x5 > 0 else 0
    y6 = mn if ((finalH > 0) and ((y1 + y2 + y3 + y4 + y5) == 0)) else 0
    finalL = y1 + y2 + y3 + y4 + y5 + y6
    mml = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dmml = (finalH - finalL) / 8.0
    mml[0] = (finalL - dmml * 2)  # Murray level -2/8
    i = 1
    while i < 13:
        mml[i] = mml[i - 1] + dmml
        i += 1
    return list(enumerate(mml))


def moving_average(sample, window, from_date, to_date):
    """
    from_date = 100, to_date = 0
    """
    data = sample.data
    wnd = float(window)
    for ind, val in enumerate(data):
        if from_date >= val.time >= to_date:
            yield sum([c.close for c in data[max(0, ind - window):ind]]) / wnd


def cos_similarity(sample, model):
    data = sample.data
    wnd = len(model)
    for ind, val in enumerate(data):
        chunk = normalize_by_min_max(make_sample(data[ind:ind+wnd]))
        if len(chunk) != len(model):
            break
        yield cosine_similarity([chunk], [model])[0][0]


# TODO. Make a renderer for a match_pattern.
# TODO. Create a better model for matching.
def murray_levels(sample, window):
    data = sample.data
    for ind, val in enumerate(data):
        yield _calc_murray_levels(data[max(0, ind - window):ind])
