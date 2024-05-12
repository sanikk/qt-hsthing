from PyQt6 import QtWidgets, QtCore

# inheritance and type hints:
from PyQt6.QtWidgets import QWidget

import random
import sys

from ui.path_tab import PathTab

class TabWindow(QtWidgets.QTabWidget):

    def __init__(self, parent: QWidget = None, path_service=None, log_service=None):
        super().__init__(parent=parent)
        self.path_service = path_service
        self.log_service = log_service

        self.resize(800, 600)
        path_tab = PathTab()
        self.addTab(path_tab, 'path tab')
        log_tab = LogTab()
        self.addTab(log_tab, 'log tab')

#     def tab_bar(self, parent=None):
#         tab_widget = QtWidgets.QTabWidget(parent=parent)
#         path_tab = None
#         self.addTab(path_tab, 'path tab')
#         log_tab = None
#         tab_widget.addTab(log_tab, 'log tab')
#         return tab_widget


class LogTab(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)


# self.text = ....
# self.button = QtWidgets.QPushButton("Click me!")
# self.layout = QtWidgets.QVBoxLayout(self)
# self.layout.addWidget(self.button)
# self.button.clicked.connect(self.magic)

#    @QtCore.pyqtSlot()
#    def magic(self):
#        self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TabWindow()
    window.setWindowTitle('silly HS thing')
    window.show()
    app.exec()
