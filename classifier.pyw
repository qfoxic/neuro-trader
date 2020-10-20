import re
import sys

import matplotlib

matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from lib.currency_strategies import moving_average
from lib.config import ConfigReader
from lib.constants import CONFIG_FILENAME
from lib.mt5client import Mt5Client


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, total, data, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.total = total
        self.ochl = data

        super().__init__(self.fig)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def compute_window_indices(self, start):
        return start, start + EVALUATION_RANGE

    def compute_initial_figure(self, start, step=450):
        self.axes.clear()
        width = 0.2
        colorup = 'k'
        colordown = 'r'
        OFFSET = width / 2.0
        end = start + step
        data = self.ochl[start:end]

        for q in data:
            t, open, close, high, low = q[:5]
            up = close >= open
            color = colorup if up else colordown
            lower = open if up else close
            height = abs(open - close)
            vline = Line2D(xdata=(t, t), ydata=(low, high), color=color, linewidth=0.5)
            rect = Rectangle(xy=(t - OFFSET, lower), width=width, height=height, facecolor=color, edgecolor=color)
            self.axes.add_line(vline)
            self.axes.add_patch(rect)

        x1, x2 = self.compute_window_indices(start)
        min_y = min(data, key=lambda x: x[-2])[-2]
        max_y = max(data, key=lambda x: x[-3])[-3]
        begin_line = Line2D(xdata=(x1, x1), ydata=(min_y, max_y), color='g', linewidth=1)
        end_line = Line2D(xdata=(x2, x2), ydata=(min_y, max_y), color='g', linewidth=1)
        self.axes.add_line(begin_line)
        self.axes.add_line(end_line)

        plot_20_ma = list(enumerate(moving_average(
            self.total, 20, self.total.data[end].time, self.total.data[start].time), start=start))
        plot_50_ma = list(enumerate(moving_average(
            self.total, 50, self.total.data[end].time, self.total.data[start].time), start=start))

        self.axes.plot([i[0] for i in plot_20_ma], [i[1] for i in plot_20_ma], '-', color='yellow')
        self.axes.plot([i[0] for i in plot_50_ma], [i[1] for i in plot_50_ma], '-', color='blue')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, total_data):
        super().__init__()
        self.stats = {
            'buy_0': 0,
            'buy_1': 0,
            'buy_2': 0,
            'buy_3': 0,
            'sell_4': 0,
            'sell_5': 0,
            'sell_6': 0,
            'sell_7': 0
        }
        self.start_pos = 200
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('Classifier')
        self.centralwidget = QtWidgets.QWidget(self)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.sc = MplCanvas(
            total_data,
            [(ind, cur.open, cur.close, cur.high, cur.low, cur.time) for ind, cur in enumerate(total_data.data)],
            self.centralwidget, width=5, height=4, dpi=100
        )
        self.sc.compute_initial_figure(self.start_pos)
        self.gridLayout.addWidget(self.sc, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.button_0 = QtWidgets.QPushButton(self.centralwidget)
        self.button_0.setText('Buy 0 strong (0)')
        self.button_0.setObjectName('buy_0')
        self.button_0.clicked.connect(self.onButtonClicked)
        self.horizontalLayout.addWidget(self.button_0)
        self.button_1 = QtWidgets.QPushButton(self.centralwidget)
        self.button_1.setText('Buy 1 (0)')
        self.button_1.setObjectName('buy_1')
        self.button_1.clicked.connect(self.onButtonClicked)
        self.horizontalLayout.addWidget(self.button_1)
        self.button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.button_2.setText('Buy 2 (0)')
        self.button_2.setObjectName('buy_2')
        self.button_2.clicked.connect(self.onButtonClicked)
        self.horizontalLayout.addWidget(self.button_2)
        self.button_3 = QtWidgets.QPushButton(self.centralwidget)
        self.button_3.setText('Buy 3 weak (0)')
        self.button_3.setObjectName('buy_3')
        self.button_3.clicked.connect(self.onButtonClicked)
        self.horizontalLayout.addWidget(self.button_3)
        self.button_4 = QtWidgets.QPushButton(self.centralwidget)
        self.button_4.setText('Sell 4 weak (0)')
        self.button_4.setObjectName('sell_4')
        self.button_4.clicked.connect(self.onButtonClicked)
        self.horizontalLayout.addWidget(self.button_4)
        self.button_5 = QtWidgets.QPushButton(self.centralwidget)
        self.button_5.setText('Sell 5 (0)')
        self.button_5.setObjectName('sell_5')
        self.button_5.clicked.connect(self.onButtonClicked)
        self.horizontalLayout.addWidget(self.button_5)
        self.button_6 = QtWidgets.QPushButton(self.centralwidget)
        self.button_6.setText('Sell 6 (0)')
        self.button_6.setObjectName('sell_6')
        self.button_6.clicked.connect(self.onButtonClicked)
        self.horizontalLayout.addWidget(self.button_6)
        self.button_7 = QtWidgets.QPushButton(self.centralwidget)
        self.button_7.setText('Sell 7 strong (0)')
        self.button_7.setObjectName('sell_7')
        self.button_7.clicked.connect(self.onButtonClicked)
        self.horizontalLayout.addWidget(self.button_7)

        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

    @QtCore.pyqtSlot()
    def onButtonClicked(self):
        sender = self.sender()
        self.stats[sender.objectName()] += 1
        sender.setText(
            re.sub(r'\(\d+\)', f'({self.stats[sender.objectName()]})', sender.text(), count=1)
        )
        with open('classified_data.txt', 'a+') as f:
            start, end = self.sc.compute_window_indices(self.start_pos)
            data = self.sc.ochl[start:end]
            f.write(f'##{sender.objectName()}\n')
            for d in data:
                row = ','.join(map(str, d[1:]))
                f.write(f'{row}\n')

        self.start_pos += MOVING_STEP
        self.sc.compute_initial_figure(self.start_pos)


qApp = QtWidgets.QApplication(sys.argv)
config = ConfigReader(CONFIG_FILENAME).load()
client = Mt5Client(config)

SYMBOL = 'EURUSD'
MOVING_STEP = 2
EVALUATION_RANGE = 26
reply = client.data(SYMBOL)
total = None

for r in reply:
    if r.sample_type == 'total':
        total = r
        break

aw = ApplicationWindow(total)
aw.setWindowTitle('Classifier')
aw.show()
sys.exit(qApp.exec_())
