from PyQt6.QtWidgets import QTabWidget, QWidget
from PyQt6.QtGui import QCloseEvent
# tähän oli joku QArgumentsParser tms
import sys

from ui.path_tab import PathTab
from ui.log_tab import LogTab


class TabWindow(QTabWidget):
    def __init__(self, parent: QWidget = None, path_service=None, log_service=None):
        super().__init__(parent=parent)
        # need this to exit cleanly?
        self._log_service = log_service

        self.resize(800, 600)
        self.setWindowTitle('silly HS thing')

        path_tab = PathTab(path_service=path_service)
        self.addTab(path_tab, 'path tab')
        log_tab = LogTab(log_service=log_service)
        self.addTab(log_tab, 'log tab')

    def closeEvent(self, event: QCloseEvent):
        self._log_service.stop_reading()
        # self._log_service.onWorkerStopped()
        event.accept()


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = TabWindow()
    window.setWindowTitle('silly HS thing')
    window.show()
    app.exec()
