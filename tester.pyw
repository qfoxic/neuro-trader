import sys

import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from lib.config import ConfigReader
from lib.constants import CONFIG_FILENAME
from lib.mt5client import Mt5Client
from lib.renderers import (CandlesRenderer, MurrayLevelsRenderer, MurrayLevelsWorkflowSignalRenderer)
from lib.workflows import (MurrayLevelBuyFlowSmaller, MurrayLevelSellFlowSmaller)


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, data_streams, x_range, parent=None, width=5, height=4):
        self.fig = Figure(figsize=(width, height))
        self.axes = self.fig.add_subplot(111)
        self.axes.set_xlim(0, x_range)
        self.data_streams = data_streams
        self.pool = QtCore.QThreadPool.globalInstance()
        super().__init__(self.fig)
        self.setParent(parent)

    def show(self):
        for data_stream in self.data_streams:
            data_stream.set_render(self)
            data_stream.setAutoDelete(False)
            self.pool.start(data_stream)

    def forward(self, to_pos):
        for data_stream in self.data_streams:
            data_stream.forward(to_pos)

    def backward(self, to_pos):
        for data_stream in self.data_streams:
            data_stream.backward(to_pos)

    def increase(self):
        for data_stream in self.data_streams:
            data_stream.increase()

    def decrease(self):
        for data_stream in self.data_streams:
            data_stream.decrease()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, data_streams, x_range):
        super().__init__()
        self.data_streams = data_streams
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('Tester')
        self.centralWidget = QtWidgets.QWidget(self)
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.sc = MplCanvas(self.data_streams, x_range, self.centralWidget, width=6, height=5)
        self.gridLayout.addWidget(self.sc, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.fwd_button = QtWidgets.QPushButton(self.centralWidget)
        self.fwd_button.setText('Forward')
        self.fwd_button.clicked.connect(self.onForwardButtonClicked)
        self.bkwd_button = QtWidgets.QPushButton(self.centralWidget)
        self.bkwd_button.setText('Backward')
        self.bkwd_button.clicked.connect(self.onBackwardButtonClicked)
        self.inc_button = QtWidgets.QPushButton(self.centralWidget)
        self.inc_button.setText('+')
        self.inc_button.clicked.connect(self.onIncreaseButtonClicked)
        self.dec_button = QtWidgets.QPushButton(self.centralWidget)
        self.dec_button.setText('-')
        self.dec_button.clicked.connect(self.onDecreaseButtonClicked)

        self.position_lineedit = QtWidgets.QLineEdit(self.centralWidget)
        self.pos_lbl = QtWidgets.QLabel('To position', self.centralWidget)
        self.pos_lbl.setBuddy(self.position_lineedit)
        self.horizontalLayout.addWidget(self.bkwd_button)
        self.horizontalLayout.addWidget(self.fwd_button)
        self.horizontalLayout.addWidget(self.pos_lbl)
        self.horizontalLayout.addWidget(self.position_lineedit)
        self.horizontalLayout.addWidget(self.inc_button)
        self.horizontalLayout.addWidget(self.dec_button)

        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.setCentralWidget(self.centralWidget)

        self.sc.show()

    @QtCore.pyqtSlot()
    def onForwardButtonClicked(self):
        pos = int(self.position_lineedit.text()) if self.position_lineedit.text() else None
        self.sc.forward(pos)
        self.sc.show()

    @QtCore.pyqtSlot()
    def onBackwardButtonClicked(self):
        pos = int(self.position_lineedit.text()) if self.position_lineedit.text() else None
        self.sc.backward(pos)
        self.sc.show()

    @QtCore.pyqtSlot()
    def onIncreaseButtonClicked(self):
        self.sc.increase()
        self.sc.show()

    @QtCore.pyqtSlot()
    def onDecreaseButtonClicked(self):
        self.sc.decrease()
        self.sc.show()


qApp = QtWidgets.QApplication(sys.argv)
config = ConfigReader(CONFIG_FILENAME).load()
client = Mt5Client(config)

SYMBOL = 'EURUSD'
WINDOW = 300

total_samples = client.data(SYMBOL)

c_render = CandlesRenderer(total_samples, WINDOW)
#ma20_render = MovingAverageRenderer(total_samples, WINDOW, 20, 'yellow')
#ma50_render = MovingAverageRenderer(total_samples, WINDOW, 50, 'blue')
#ma120_render = MovingAverageRenderer(total_samples, WINDOW, 120, 'red')
#maw_render = ThreeMAWorkflowRenderer(total_samples, WINDOW)
murray_render = MurrayLevelsRenderer(total_samples, WINDOW)
murray_wsrender = MurrayLevelsWorkflowSignalRenderer(total_samples, WINDOW, 'red', MurrayLevelSellFlowSmaller, 10)
murray_wbrender = MurrayLevelsWorkflowSignalRenderer(total_samples, WINDOW, 'blue', MurrayLevelBuyFlowSmaller, 3)
#murray_wsrender = MurrayLevelsWorkflowSellRenderer(total_samples, WINDOW)

aw = ApplicationWindow([
    c_render,
    #murray_render,
    # murray_wbrender,
    murray_wbrender,
    #ma20_render, ma50_render, ma120_render,
    #maw_render
], WINDOW)
aw.setWindowTitle('Tester')
aw.show()

sys.exit(qApp.exec_())


# TODO. Based on analyzer classes make a dashboard that will take values from metatrader, discover the best entry
#  point based on analyzer and put "one" in a table. !!!!
# TODO. Add button classify which will take highlighted region and classify it as specified.
# TODO. Try to make a pipeline: cosine sim -> check if this is a daily lowest/highest point -> send SMS.
