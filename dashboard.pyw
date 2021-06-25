import queue
import sys

from PyQt5.QtWidgets import (QApplication)

from lib.config import ConfigReader
from lib.constants import CONFIG_FILENAME
from lib.currency_datatypes import Command
from lib.currency_loader import CurrenciesLoader
from lib.currency_processor import CurrenciesProcessor
from lib.mainwindow import MainWindow
from lib.mt5client import Mt5Client


if __name__ == '__main__':
    app = QApplication(sys.argv)
    config = ConfigReader(CONFIG_FILENAME).load()
    tabs_config = ConfigReader(CONFIG_FILENAME).tabs()
    main_queue = queue.Queue()
    commands_queue = queue.Queue()
    mainWin = MainWindow()

    for i, tab_id in enumerate(tabs_config):
        s = config[tab_id]
        mainWin.addTab(i, s['name'], tab_id, s['labels'])
        commands_queue.put_nowait(Command(tab_id=tab_id, command='rates', currencies=','.join(s['currencies'])))

    mainWin.show()

    loader = CurrenciesLoader(app, queue=main_queue, client=Mt5Client(config), config=tabs_config,
                              commands_queue=commands_queue)
    processor = CurrenciesProcessor(app, queue=main_queue, config=tabs_config)
    loader.start()
    processor.start()
    processor.dataProcessed.connect(mainWin.onCurrencyDataProcessed)
    mainWin.refreshButtonClicked.connect(
        lambda tab: commands_queue.put_nowait(
            Command(tab_id=tab, command='rates', currencies=','.join(config[tab]['currencies']))
        )
    )
    mainWin.chartButtonClicked.connect(
        lambda tab, currency: commands_queue.put_nowait(
            Command(tab_id=tab, command='chart', currencies=currency)
        )
    )
    sys.exit(app.exec_())

# TODO. Instead of merging levels let's merge closest prices together.
