# Used only to add some large number to support line to ensure it will appear
SUPPORT_LINE_MAXIMUM_AMOUNT = 600

BARS = 600
CLOSEST_SUPPORT_THRESHOLD = 20
SLOPE_THRESHOLD = 0.3

CONFIG_FILENAME = './config.ini'

CLASSIFIED_SAMPLE_NAMES = [
    '##buy_0', '##buy_1', '##buy_2', '##buy_3',
    '##sell_4', '##sell_5', '##sell_6', '##sell_7'
]

RENDERER_STEP = 200
EVALUATION_RANGE = 40
VIEW_RANGE = 450
COSINE_SIMILARITY_PRECISE = 0.98

MURRAY_LEVELS_MAP = {
    0: '-2',
    1: '-1',
    2: '0',
    3: '1',
    4: '2',
    5: '3',
    6: '4',
    7: '5',
    8: '6',
    9: '7',
    10: '8',
    11: '+1',
    12: '+2'
}
