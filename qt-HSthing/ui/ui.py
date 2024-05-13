from PyQt6 import QtWidgets, QtCore

# inheritance and type hints:
from PyQt6.QtWidgets import QWidget

import random
import sys

from ui.path_tab import PathTab
from ui.log_tab import LogTab


class TabWindow(QtWidgets.QTabWidget):
    def __init__(self, parent: QWidget = None, path_service=None, log_service=None):
        super().__init__(parent=parent)
        self.path_service = path_service
        self.log_service = log_service

        self.resize(800, 600)
        self.setWindowTitle('silly HS thing')

        path_tab = PathTab(path_service=path_service)
        self.addTab(path_tab, 'path tab')
        log_tab = LogTab(log_service=log_service)
        self.addTab(log_tab, 'log tab')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TabWindow()
    window.setWindowTitle('silly HS thing')
    window.show()
    app.exec()
