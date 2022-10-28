from PyQt5.QtCore import QRect, pyqtSlot, pyqtSignal, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QMainWindow, QWidget, QGridLayout, QMenuBar, QStatusBar, QTabWidget,
                             QTableView, QHeaderView, QHBoxLayout, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy)

from lib.currency_datatypes import CurrencyProcessed


class SortingProxyModel(QSortFilterProxyModel):
    def lessThan(self, left, right):
        left_data = self.sourceModel().data(left)
        right_data = self.sourceModel().data(right)

        if left_data[0].isalpha():
            return left_data < right_data
        else:
            return float(left_data) < float(right_data)


class MainWindow(QMainWindow):
    refreshButtonClicked = pyqtSignal(str)
    chartButtonClicked = pyqtSignal(str, str)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.models = {}
        self.views = {}
        self.labels = {}
        self.resize(1079, 829)
        self.centralwidget = QWidget(self)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 1079, 26))
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

    def addTab(self, index, title, tab_id, labels):
        tab = QWidget()
        horizontalLayout = QHBoxLayout(tab)
        tableView = QTableView(tab)
        horizontalLayout.addWidget(tableView)
        verticalLayout = QVBoxLayout()
        refreshButton = QPushButton('Refresh', tab)
        refreshButton.setObjectName(f'{tab_id}:rates')
        chartButton = QPushButton('Chart', tab)
        chartButton.setObjectName(f'{tab_id}:chart')
        verticalLayout.addWidget(refreshButton)
        verticalLayout.addWidget(chartButton)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        verticalLayout.addItem(verticalSpacer)
        horizontalLayout.addLayout(verticalLayout)

        sortModel = SortingProxyModel(tab)
        model = QStandardItemModel(tab)
        model.setHorizontalHeaderLabels(labels)
        sortModel.setSourceModel(model)

        tableView.setModel(sortModel)
        tableView.setSortingEnabled(True)
        tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Do not display columns with _
        for _id, label in enumerate(labels):
            if label.startswith('_'):
                tableView.setColumnHidden(_id, True)

        self.tabWidget.addTab(tab, tab_id)
        self.tabWidget.setTabText(index, title)

        refreshButton.clicked.connect(self.onRefreshButtonClicked)
        chartButton.clicked.connect(self.onChartButtonClicked)

        self.models[tab_id] = model
        self.views[tab_id] = tableView
        self.labels[tab_id] = labels

    @pyqtSlot(CurrencyProcessed)
    def onCurrencyDataProcessed(self, data):
        model = self.models[data.group]
        metrics = data.metrics
        model.appendRow((
            QStandardItem(data.currency), *[QStandardItem(val) for val in metrics.values()])
        )

    def onRefreshButtonClicked(self):
        tab_id = self.sender().objectName().split(':')[0]
        model = self.models[tab_id]
        model.removeRows(0, model.rowCount())
        self.refreshButtonClicked.emit(tab_id)

    def onChartButtonClicked(self):
        tab_id = self.sender().objectName().split(':')[0]
        view = self.views[tab_id]
        cur_index = view.currentIndex()
        if cur_index.isValid():
            data = [cur_index.sibling(cur_index.row(), 0).data()]
            for i, label in enumerate(self.labels[tab_id]):
                if label.startswith('_'):
                    data.append(cur_index.sibling(cur_index.row(), i).data())
            # [CURRENCY, SUPPORTS levels]
            self.chartButtonClicked.emit(tab_id, ','.join(data))
# TODO. Add loading indicator to statusbar
# TODO. Add filters UI tables on a currency.
# TODO. Compile all python files and think on a distribution
# TODO. Add kind of licensing
# TODO. On currency click add open url.
