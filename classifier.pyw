import sys

import matplotlib

matplotlib.use('QtAgg')
from PyQt6 import QtCore, QtWidgets

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from lib.config import ConfigReader
from lib.constants import CONFIG_FILENAME, EVALUATION_RANGE
from lib.mt5client import Mt5Client


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.evaluation_range = EVALUATION_RANGE
        self.total = []
        self.ochl = []

        super().__init__(self.fig)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(
            self, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def setCurrencyData(self, total):
        self.total = total
        self.ochl = [
            (ind, cur.open, cur.close, cur.high, cur.low, cur.time) for ind, cur in enumerate(self.total.data)
        ]

    def compute_window_indices(self, start):
        return start, start + self.evaluation_range

    def compute_initial_figure(self, start, step=450, evaluation_range=None):
        self.axes.clear()
        width = 0.2
        colorup = 'k'
        colordown = 'r'
        OFFSET = width / 2.0
        end = start + step
        data = self.ochl[start:end]
        self.evaluation_range = evaluation_range if evaluation_range else self.evaluation_range
        if not data:
            return
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

        x1, x2 = start, start + self.evaluation_range
        min_y = min(data, key=lambda x: x[-2])[-2]
        max_y = max(data, key=lambda x: x[-3])[-3]
        begin_line = Line2D(xdata=(x1, x1), ydata=(min_y, max_y), color='g', linewidth=1)
        end_line = Line2D(xdata=(x2, x2), ydata=(min_y, max_y), color='g', linewidth=1)
        self.axes.add_line(begin_line)
        self.axes.add_line(end_line)
        self.axes.plot()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_pos = 0
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowTitle('Classifier')
        self.centralwidget = QtWidgets.QWidget(self)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.sc = MplCanvas(self.centralwidget, width=5, height=4, dpi=100)
        self.gridLayout.addWidget(self.sc, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayoutForLoadControls = QtWidgets.QHBoxLayout()
        self.horizontalLayoutForMoveControls = QtWidgets.QHBoxLayout()

        self.classifyButton = QtWidgets.QPushButton(self.centralwidget)
        self.classifyButton.setText('Classify')
        self.classifyButton.setObjectName('classifyButton')
        self.classifyButton.clicked.connect(self.onClassifyButtonClicked)
        self.horizontalLayout.addWidget(self.classifyButton)

        self.startPosLabel = QtWidgets.QLabel(self.centralwidget)
        self.startPosLabel.setObjectName('startPosLabel')
        self.startPosLabel.setText('Pos')
        self.startPosLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.startPosLineEdit.setObjectName('startPosLineEdit')
        self.startPosLabel.setBuddy(self.startPosLineEdit)

        self.evaluationLabel = QtWidgets.QLabel(self.centralwidget)
        self.evaluationLabel.setObjectName('evaluationLabel')
        self.evaluationLabel.setText('Evaluation range')
        self.evaluationRangeLE = QtWidgets.QLineEdit(self.centralwidget)
        self.evaluationRangeLE.setObjectName('evaluationRangeLE')
        self.evaluationLabel.setBuddy(self.evaluationRangeLE)

        self.forwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.forwardButton.setObjectName('forwardButton')
        self.forwardButton.setText('Forward')
        self.forwardButton.setToolTip('Move graph forward')
        self.forwardButton.clicked.connect(self.onForwardButtonClicked)
        self.jumpButton = QtWidgets.QPushButton(self.centralwidget)
        self.jumpButton.setObjectName('jumpButton')
        self.jumpButton.setText('Jump to')
        self.jumpButton.setToolTip('Jump to a specified position')
        self.jumpButton.clicked.connect(self.onJumpButtonClicked)
        self.backwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.backwardButton.setObjectName('backwardButton')
        self.backwardButton.setText('Backward')
        self.backwardButton.setToolTip('Move graph backward')
        self.backwardButton.clicked.connect(self.onBackwardButtonClicked)

        self.loadCurrencyBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loadCurrencyBtn.setObjectName('loadCurrencyBtn')
        self.loadCurrencyBtn.setText('Load')
        self.loadCurrencyBtn.setToolTip('Load currency data into this application')
        self.loadCurrencyBtn.clicked.connect(self.onLoadCurrencyButtonClicked)

        self.currencyWidget = QtWidgets.QComboBox(self.centralwidget)
        self.currencyWidget.setObjectName('currencyWidget')
        self.currencyWidget.addItems(config['common']['currencies'])

        self.periodWidget = QtWidgets.QComboBox(self.centralwidget)
        self.periodWidget.setObjectName('periodWidget')
        self.periodWidget.addItems(config['common']['timeframes'])

        self.horizontalLayoutForLoadControls.addWidget(self.currencyWidget)
        self.horizontalLayoutForLoadControls.addWidget(self.periodWidget)
        self.horizontalLayoutForLoadControls.addWidget(self.evaluationLabel)
        self.horizontalLayoutForLoadControls.addWidget(self.evaluationRangeLE)
        self.horizontalLayoutForLoadControls.addWidget(self.loadCurrencyBtn)

        self.horizontalLayoutForMoveControls.addWidget(self.jumpButton)
        self.horizontalLayoutForMoveControls.addWidget(self.startPosLabel)
        self.horizontalLayoutForMoveControls.addWidget(self.startPosLineEdit)
        self.horizontalLayoutForMoveControls.addWidget(self.backwardButton)
        self.horizontalLayoutForMoveControls.addWidget(self.forwardButton)

        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayoutForLoadControls, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayoutForMoveControls, 3, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

    def loadData(self, total):
        self.sc.setCurrencyData(total)
        try:
            evaluation_range = int(self.evaluationRangeLE.text())
        except ValueError:
            evaluation_range = None
        self.sc.compute_initial_figure(self.start_pos, evaluation_range=evaluation_range)

    @QtCore.pyqtSlot()
    def onClassifyButtonClicked(self):
        with open(f'classified_figure_{self.currencyWidget.currentText().upper()}.txt', 'a+') as f:
            start, end = self.sc.compute_window_indices(self.start_pos)
            data = self.sc.ochl[start:end]
            for d in data:
                row = '\t'.join(map(str, d[1:]))
                f.write(f'{row}\n')

    @QtCore.pyqtSlot()
    def onLoadCurrencyButtonClicked(self):
        currency = self.currencyWidget.currentText()
        period = self.periodWidget.currentText()
        self.start_pos = int(self.startPosLineEdit.text() or 0)
        client.rates_all_stored(currency, period, f'data_{currency.upper()}')
        self.loadData(client.data(currency))

    @QtCore.pyqtSlot()
    def onForwardButtonClicked(self):
        self.start_pos += 1
        if self.start_pos > len(self.sc.total.data):
            return
        self.sc.compute_initial_figure(self.start_pos)

    @QtCore.pyqtSlot()
    def onBackwardButtonClicked(self):
        self.start_pos -= 1
        if self.start_pos < 0:
            return
        self.sc.compute_initial_figure(self.start_pos)

    @QtCore.pyqtSlot()
    def onJumpButtonClicked(self):
        tmp_pos = self.start_pos
        try:
            self.start_pos = int(self.startPosLineEdit.text())
        except ValueError:
            self.start_pos = tmp_pos
        self.sc.compute_initial_figure(self.start_pos)


qApp = QtWidgets.QApplication(sys.argv)
config = ConfigReader(CONFIG_FILENAME).load()
client = Mt5Client(config)

aw = ApplicationWindow()
aw.setWindowTitle('Classifier')
aw.show()
sys.exit(qApp.exec())
