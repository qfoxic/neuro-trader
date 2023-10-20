import os
import glob
import numpy as np
from functools import cache
from mcorelib.utils import data, normalize_by_min_max


def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)

    if norm_vector1 != 0 and norm_vector2 != 0:
        return dot_product / (norm_vector1 * norm_vector2)
    else:
        return 0  # If any of the vectors is a zero vector, return 0


def cos_similarity_score(sample, model):
    pattern = normalize_by_min_max(sample)
    model_length = len(model)
    pattern_length = len(pattern)
    if pattern_length > model_length:
        # If pattern is larger than take last portion of a pattern by model length and compare it
        return cosine_similarity(pattern[-model_length:], model)
    if pattern_length < model_length:
        return 0.0
    return cosine_similarity(pattern, model)


@cache
def load_trade_models(mirror=False):
    # By default we have to present only buy models
    return {
        os.path.basename(model): normalize_by_min_max(
            data('empty', model).mirror() if mirror else data('empty', model))
        for model in glob.glob(os.path.join('.', 'trademodels', '*'))
    }
