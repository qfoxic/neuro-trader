import sys

import matplotlib

matplotlib.use('QtAgg')
from PyQt6 import QtCore, QtWidgets

import matplotlib.style as mplstyle
mplstyle.use('fast')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from lib.config import ConfigReader
from lib.constants import CONFIG_FILENAME, EVALUATION_RANGE, VIEW_RANGE
from lib.mt5client import Mt5Client
from lib.currency.utils import normalize_by_min_max
from lib.currency.indicators import cos_similarity

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=7, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.evaluation_range = EVALUATION_RANGE
        self.view_range = VIEW_RANGE
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

    def increment_eval_range(self):
        self.evaluation_range += 1

    def decrement_eval_range(self):
        self.evaluation_range -= 1

    def increment_view_range(self):
        self.view_range += 100

    def decrement_view_range(self):
        self.view_range -= 100

    def compute_initial_figure(self, start):
        self.axes.clear()
        width = 0.2
        colorup = 'k'
        colordown = 'r'
        OFFSET = width / 2.0
        end = start + self.view_range
        data = self.ochl[start:end]
        if not data:
            return
        for q in data:
            t, open, close, high, low = q[:5]
            up = close >= open
            color = colorup if up else colordown
            lower = open if up else close
            height = abs(open - close)
            vline = Line2D(xdata=(t, t), ydata=(low, high), color=color, linewidth=0.5, markevery=100)
            rect = Rectangle(xy=(t - OFFSET, lower), width=width, height=height, facecolor=color, edgecolor=color)
            self.axes.add_line(vline)
            self.axes.add_patch(rect)

        x1, x2 = start, start + self.evaluation_range
        min_y = min(data, key=lambda x: x[-2])[-2]
        max_y = max(data, key=lambda x: x[-3])[-3]
        begin_line = Line2D(xdata=(x1, x1), ydata=(min_y, max_y), color='g', linewidth=1, markevery=100)
        end_line = Line2D(xdata=(x2, x2), ydata=(min_y, max_y), color='g', linewidth=1, markevery=100)
        self.axes.add_line(begin_line)
        self.axes.add_line(end_line)
        self.axes.plot()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_pos = 0
        self.matched_figures_index = 0
        self.matched_figures = []
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowTitle('Classifier')
        self.centralwidget = QtWidgets.QWidget(self)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.sc = MplCanvas(self.centralwidget, width=5, height=4, dpi=100)
        self.gridLayout.addWidget(self.sc, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayoutForLoadControls = QtWidgets.QHBoxLayout()
        self.horizontalLayoutForMoveControls = QtWidgets.QHBoxLayout()
        self.horizontalLayoutForMatchControls = QtWidgets.QHBoxLayout()

        self.viewDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.viewDataButton.setText('View Data')
        self.viewDataButton.setObjectName('viewDataButton')
        self.viewDataButton.setToolTip('Load data from a local file')
        self.viewDataButton.clicked.connect(self.onLoadStoredButtonClicked)

        self.findPositionsButton = QtWidgets.QPushButton(self.centralwidget)
        self.findPositionsButton.setText('Run matching algorithm')
        self.findPositionsButton.setObjectName('findPositionsButton')
        self.findPositionsButton.clicked.connect(self.onFindPositionsButtonClicked)

        self.nextFigureButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextFigureButton.setText('Next Figure')
        self.nextFigureButton.setObjectName('nextFigureButton')
        self.nextFigureButton.clicked.connect(self.onNextFigureButtonClicked)
        self.nextFigureButton.setDisabled(True)

        self.prevFigureButton = QtWidgets.QPushButton(self.centralwidget)
        self.prevFigureButton.setText('Previous Figure')
        self.prevFigureButton.setObjectName('prevFigureButton')
        self.prevFigureButton.clicked.connect(self.onPrevFigureButtonClicked)
        self.prevFigureButton.setDisabled(True)

        self.classifyButton = QtWidgets.QPushButton(self.centralwidget)
        self.classifyButton.setText('Classify')
        self.classifyButton.setObjectName('classifyButton')
        self.classifyButton.setToolTip('Store selected region of candles in a classified_figure_CURRENCY.txt file')
        self.classifyButton.clicked.connect(self.onClassifyButtonClicked)

        self.increaseRangeButton = QtWidgets.QPushButton(self.centralwidget)
        self.increaseRangeButton.setText('Range +')
        self.increaseRangeButton.setObjectName('increaseRangeButton')
        self.increaseRangeButton.setToolTip('Enlarge evaluation range')
        self.increaseRangeButton.clicked.connect(self.onIncRangeButtonClicked)

        self.increaseViewButton = QtWidgets.QPushButton(self.centralwidget)
        self.increaseViewButton.setText('View +')
        self.increaseViewButton.setObjectName('increaseViewButton')
        self.increaseViewButton.setToolTip('Zoom view in')
        self.increaseViewButton.clicked.connect(self.onIncViewButtonClicked)

        self.decreaseViewButton = QtWidgets.QPushButton(self.centralwidget)
        self.decreaseViewButton.setText('View -')
        self.decreaseViewButton.setObjectName('decreaseViewButton')
        self.decreaseViewButton.setToolTip('Zoom view out')
        self.decreaseViewButton.clicked.connect(self.onDecrViewButtonClicked)

        self.decreaseRangeButton = QtWidgets.QPushButton(self.centralwidget)
        self.decreaseRangeButton.setText('Range -')
        self.decreaseRangeButton.setObjectName('decreaseRangeButton')
        self.decreaseRangeButton.setToolTip('Shrink evaluation range')
        self.decreaseRangeButton.clicked.connect(self.onDecrRangeButtonClicked)

        self.viewModelButton = QtWidgets.QPushButton(self.centralwidget)
        self.viewModelButton.setText('View Model')
        self.viewModelButton.setObjectName('viewModelButton')
        self.viewModelButton.setToolTip('Display classified figure')
        self.viewModelButton.clicked.connect(self.onViewModelButtonClicked)

        self.startPosLabel = QtWidgets.QLabel(self.centralwidget)
        self.startPosLabel.setObjectName('startPosLabel')
        self.startPosLabel.setText('Pos')
        self.startPosLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.startPosLineEdit.setObjectName('startPosLineEdit')
        self.startPosLabel.setBuddy(self.startPosLineEdit)

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
        self.loadCurrencyBtn.setText('Load from MT5')
        self.loadCurrencyBtn.setToolTip('Load currency data into this application')
        self.loadCurrencyBtn.clicked.connect(self.onLoadCurrencyButtonClicked)

        self.currencyWidget = QtWidgets.QComboBox(self.centralwidget)
        self.currencyWidget.setObjectName('currencyWidget')
        self.currencyWidget.addItems(config['common']['currencies'])

        self.periodWidget = QtWidgets.QComboBox(self.centralwidget)
        self.periodWidget.setObjectName('periodWidget')
        self.periodWidget.addItems(config['common']['timeframes'])

        self.horizontalLayout.addWidget(self.viewDataButton)
        self.horizontalLayout.addWidget(self.viewModelButton)
        self.horizontalLayout.addWidget(self.classifyButton)
        self.horizontalLayout.addWidget(self.increaseRangeButton)
        self.horizontalLayout.addWidget(self.decreaseRangeButton)
        self.horizontalLayout.addWidget(self.increaseViewButton)
        self.horizontalLayout.addWidget(self.decreaseViewButton)
        self.horizontalLayoutForLoadControls.addWidget(self.currencyWidget)
        self.horizontalLayoutForLoadControls.addWidget(self.periodWidget)
        self.horizontalLayoutForLoadControls.addWidget(self.loadCurrencyBtn)

        self.horizontalLayoutForMatchControls.addWidget(self.findPositionsButton)
        self.horizontalLayoutForMatchControls.addWidget(self.prevFigureButton)
        self.horizontalLayoutForMatchControls.addWidget(self.nextFigureButton)

        self.horizontalLayoutForMoveControls.addWidget(self.jumpButton)
        self.horizontalLayoutForMoveControls.addWidget(self.startPosLabel)
        self.horizontalLayoutForMoveControls.addWidget(self.startPosLineEdit)
        self.horizontalLayoutForMoveControls.addWidget(self.backwardButton)
        self.horizontalLayoutForMoveControls.addWidget(self.forwardButton)

        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayoutForMatchControls, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayoutForLoadControls, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayoutForMoveControls, 4, 0, 1, 1)

        self.setCentralWidget(self.centralwidget)

    def loadData(self):
        currency = self.currencyWidget.currentText()
        self.start_pos = int(self.startPosLineEdit.text() or 0)
        total = client.data(currency, f'data_{currency.upper()}')
        self.sc.setCurrencyData(total)
        self.sc.compute_initial_figure(self.start_pos)

    def loadModel(self):
        currency = self.currencyWidget.currentText()
        self.start_pos = 0
        total = client.data(currency, f'classified_figure_{currency.upper()}.txt')
        self.sc.setCurrencyData(total)
        self.sc.compute_initial_figure(self.start_pos)

    @QtCore.pyqtSlot()
    def onClassifyButtonClicked(self):
        with open(f'classified_figure_{self.currencyWidget.currentText().upper()}.txt', 'a+') as f:
            start, end = self.sc.compute_window_indices(self.start_pos)
            data = self.sc.ochl[start:end]
            for d in data:
                row = '\t'.join(map(str, d[1:]))
                f.write(f'{row}\n')

    @QtCore.pyqtSlot()
    def onFindPositionsButtonClicked(self):
        currency = self.currencyWidget.currentText()
        total_samples = client.data(currency, f'data_{currency.upper()}')

        model = normalize_by_min_max(client.data(currency, f'classified_figure_{currency.upper()}.txt'))
        cos_sim_stream = enumerate(cos_similarity(total_samples, model))

        for ind, sim in cos_sim_stream:
            if sim > 0.98:
                self.matched_figures.append([ind, sim])
        self.nextFigureButton.setDisabled(False)
        print(self.matched_figures)
        if not self.sc.ochl:
            self.loadData()

    @QtCore.pyqtSlot()
    def onPrevFigureButtonClicked(self):
        if self.matched_figures_index <= 0:
            self.prevFigureButton.setDisabled(True)
            self.matched_figures_index = 0
            return

        self.start_pos = self.matched_figures[self.matched_figures_index][0]
        self.sc.compute_initial_figure(self.start_pos)
        self.matched_figures_index -= 1
        self.nextFigureButton.setEnabled(True)

    @QtCore.pyqtSlot()
    def onNextFigureButtonClicked(self):
        if self.matched_figures_index >= len(self.matched_figures) - 1:
            self.nextFigureButton.setDisabled(True)
            return

        self.start_pos = self.matched_figures[self.matched_figures_index][0]
        self.sc.compute_initial_figure(self.start_pos)
        self.matched_figures_index += 1
        self.prevFigureButton.setEnabled(True)

    @QtCore.pyqtSlot()
    def onViewModelButtonClicked(self):
        self.loadModel()

    @QtCore.pyqtSlot()
    def onIncRangeButtonClicked(self):
        self.sc.increment_eval_range()
        self.sc.compute_initial_figure(self.start_pos)

    @QtCore.pyqtSlot()
    def onIncViewButtonClicked(self):
        self.sc.increment_view_range()
        self.sc.compute_initial_figure(self.start_pos)

    @QtCore.pyqtSlot()
    def onDecrViewButtonClicked(self):
        self.sc.decrement_view_range()
        self.sc.compute_initial_figure(self.start_pos)

    @QtCore.pyqtSlot()
    def onDecrRangeButtonClicked(self):
        self.sc.decrement_eval_range()
        self.sc.compute_initial_figure(self.start_pos)

    @QtCore.pyqtSlot()
    def onLoadCurrencyButtonClicked(self):
        currency = self.currencyWidget.currentText()
        period = self.periodWidget.currentText()
        client.rates_all_stored(currency, period, f'data_{currency.upper()}')
        self.loadData()

    @QtCore.pyqtSlot()
    def onLoadStoredButtonClicked(self):
        self.loadData()

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
