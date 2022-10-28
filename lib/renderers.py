from PyQt6.QtCore import QRunnable
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from lib.constants import RENDERER_STEP
from lib.currency.streams import (
    EnumeratedMovingAveragePricesStream, EnumeratedCandlesStream, EnumeratedMurrayLevelsStream,
    EnumeratedCosineSimilarityStream
)
from lib.workflows import MurrayLevelsSignal


class BaseRenderer(QRunnable):
    def __init__(self, sample, x_range, step=None):
        super().__init__()
        self.candles_stream = sample.data
        self.sample = sample
        self.x_range = x_range
        self.step = step or RENDERER_STEP
        self.start_pos = 0
        self.last_pos = 0
        self.data_iter = self.get_iter()
        self.canvas = None

    def get_iter(self):
        raise NotImplementedError()

    def forward(self, to=None):
        if to:
            self.start_pos = to
        else:
            self.start_pos += self.step

    def backward(self, to=None):
        if to:
            self.start_pos = to
        else:
            self.start_pos -= self.step

    def increase(self):
        self.x_range += 100

    def decrease(self):
        if self.x_range > 200:
            self.x_range -= 100

    def set_render(self, canvas):
        self.canvas = canvas

    def render(self, canvas):
        pass

    def run(self):
        try:
            self.render(self.canvas)
        except StopIteration:
            print('No data in streams')
        self.canvas.fig.canvas.flush_events()
        self.canvas.fig.canvas.draw_idle()


class CandlesRenderer(BaseRenderer):
    def __init__(self, sample, x_range):
        super().__init__(sample, x_range)

    def get_iter(self):
        return iter(EnumeratedCandlesStream(self.sample))

    def render(self, canvas):
        width = 0.2
        colorup = 'k'
        colordown = 'r'
        OFFSET = width / 2.0

        end = self.start_pos + self.x_range
        current_slice = self.candles_stream[self.start_pos:end]
        max_price = max(current_slice, key=lambda o: o.high).high
        min_price = min(current_slice, key=lambda o: o.low).low
        canvas.axes.set_ylim(min_price, max_price)
        canvas.axes.set_xlim(self.start_pos, end)

        while self.last_pos < end:
            num, price = next(self.data_iter)
            t, open, close, high, low = num, price.open, price.close, price.high, price.low
            up = close >= open
            color = colorup if up else colordown
            lower = open if up else close
            height = abs(open - close)
            canvas.axes.add_line(
                Line2D(xdata=(t, t), ydata=(low, high), color=color, linewidth=0.5, antialiased=False))
            canvas.axes.add_patch(
                Rectangle(xy=(t - OFFSET, lower), antialiased=False,
                          width=width, height=height, facecolor=color, edgecolor=color))
            self.last_pos += 1


class MovingAverageRenderer(BaseRenderer):
    def __init__(self, sample, x_range, period, color):
        self.period = period
        self.color = color
        super().__init__(sample, x_range)

    def get_iter(self):
        return iter(EnumeratedMovingAveragePricesStream(self.sample, self.period))

    def render(self, canvas):
        end = self.start_pos + self.x_range
        while self.last_pos < end:
            num, price = next(self.data_iter)
            canvas.axes.add_line(
                Line2D(xdata=[num, num + 1], ydata=[price, price], color=self.color, antialiased=False,
                       linewidth=1, linestyle='-'))
            self.last_pos += 1


class CosineSimilarityRenderer(BaseRenderer):
    def __init__(self, sample, x_range, model):
        self.model = model
        super().__init__(sample, x_range)

    def get_iter(self):
        return iter(EnumeratedCosineSimilarityStream(self.sample, self.model))

    def render(self, canvas):
        end = self.start_pos + self.x_range
        while self.last_pos < end:
            num, sim = next(self.data_iter)
            if sim > 0.97:
                canvas.axes.add_line(
                    Line2D(xdata=[num, num + 1], ydata=[0, self.sample.max_price], color='green', antialiased=False,
                           linewidth=1, linestyle='-'))
                canvas.axes.add_line(
                    Line2D(xdata=[num+len(self.model), num+len(self.model) + 1], ydata=[0, self.sample.max_price], color='red', antialiased=False,
                           linewidth=1, linestyle='-'))
            self.last_pos += 1
# TODO. Polish matching model

class MurrayLevelsRenderer(BaseRenderer):
    def __init__(self, sample, x_range, period=200):
        self.period = period
        self.last_x = 0
        self.last_lvl_0_price = -1
        super().__init__(sample, x_range)

    def get_iter(self):
        return iter(EnumeratedMurrayLevelsStream(self.sample, self.period))

    def render(self, canvas):
        end = self.start_pos + self.x_range
        while self.last_pos < end:
            pos, mml = next(self.data_iter)
            for lvl, m in mml:
                canvas.axes.add_line(
                    Line2D(xdata=[pos, pos + 1], ydata=[m, m], color='green', antialiased=False,
                           linewidth=1, linestyle='-'))
                # canvas.axes.text(x=pos, y=m, s=MURRAY_LEVELS_MAP[lvl])

            # lvl_0_price = mml[0] if mml else 0
            # if self.last_lvl_0_price != lvl_0_price:
            #    for lvl, m in mml:
            #        canvas.axes.add_line(
            #            Line2D(xdata=[self.last_x, pos + 1], ydata=[m, m], color='green', antialiased=False,
            #                   linewidth=1, linestyle='-'))
            #        canvas.axes.text(x=pos, y=m, s=MURRAY_LEVELS_MAP[lvl])
            #    self.last_lvl_0_price = lvl_0_price
            #    self.last_x = pos

            self.last_pos += 1


class MurrayLevelsWorkflowSignalRenderer(BaseRenderer):
    def __init__(self, sample, x_range, color, flow_class, trigger_level):
        self.workflow = MurrayLevelsSignal(sample, flow_class, trigger_level)
        self.color = color
        super().__init__(sample, x_range)

    def get_iter(self):
        return None

    def render(self, canvas):
        end = self.start_pos + self.x_range
        while self.last_pos < end:
            pos = self.workflow.move()
            if pos >= 0:
                canvas.axes.add_line(
                    Line2D(xdata=[pos, pos], ydata=[self.sample.min_price, self.sample.max_price],
                           color=self.color, linewidth=1, linestyle='-', antialiased=False))
            self.last_pos += 1
