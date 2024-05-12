from PyQt6 import QtWidgets

# inheritance and type hints:
from PyQt6.QtWidgets import QWidget

import sys


class PathTab(QWidget):
    def __init__(self, parent=None, path_service=None):
        super().__init__(parent=parent)

        self._path_service = path_service

        layout = QtWidgets.QVBoxLayout()

        path_title_label = QtWidgets.QLabel('Log path')
        layout.addWidget(path_title_label)
        # log_path_label = QtWidgets.QLabel(self._path_service.get_log_path())
        log_path_dialog_button = QtWidgets.QPushButton('set path')
        layout.addWidget(log_path_dialog_button)
        # command=self._log_path_dialog
        log_path_save_button = QtWidgets.QPushButton('save path')
        layout.addWidget(log_path_save_button)
        # command=self._path_service.save_log_path

        self.setLayout(layout)

    def _log_path_dialog(self):
        pass


def _get_log_path_box(self, master=None):
    container = LabelFrame(master=master)

    path_title_label = Label(master=container, text='Log path')
    self.log_path_label = Label(master=container, text=self._path_service.get_log_path())
    log_path_dialog_button = Button(master=container, text='set path', command=self._log_path_dialog)
    log_path_save_button = Button(master=container, text='save path', command=self._path_service.save_log_path)

    path_title_label.grid(row=0, column=0, sticky='ew')
    self.log_path_label.grid(row=0, column=1)
    log_path_dialog_button.grid(row=0, column=2, sticky='ew')
    log_path_save_button.grid(row=0, column=3, sticky='ew')

    subdir_title_label = Label(master=container, text='Used subdir')
    self.log_subdir_label = Label(master=container, text=self._path_service.get_subdir_name())
    subdir_reset_button = Button(master=container, text='reset subdir', command=self._set_subdir())

    subdir_title_label.grid(row=1, column=0, sticky='ew')
    self.log_subdir_label.grid(row=1, column=1)
    subdir_reset_button.grid(row=1, column=2, sticky='ew')

    return container




class MockService:
    def get_subdir_name(self):
        return 'subdir name'

    def get_log_path(self):
        return '/log/path/'



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PathTab(path_service=mockservice)
    # mabbe should calculate the actual value, 800 - padding etc, 600 - padding etc
    window.resize(800, 600)
    window.setWindowTitle('silly HS thing')

    window.show()
    app.exec()
