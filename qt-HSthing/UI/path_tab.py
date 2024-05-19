from PyQt6.QtWidgets import QFileDialog, QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout, QPushButton

import sys


class PathTab(QWidget):
    def __init__(self, parent=None, path_service=None):
        super().__init__(parent=parent)
        self._path_service = path_service

        layout = QVBoxLayout()

        log_path_title_label = QLabel('Log path')
        layout.addWidget(log_path_title_label)
        self.log_path_value_label = QLabel(self._path_service.get_log_path())
        layout.addWidget(self.log_path_value_label)

        subdir_title_label = QLabel('Used subdir')
        layout.addWidget(subdir_title_label)
        self.subdir_value_label = QLabel(self._path_service.get_subdir_name())
        layout.addWidget(self.subdir_value_label)

        buttons_group = self.get_buttons_group_box()
        layout.addWidget(buttons_group)

        self.setLayout(layout)

    def get_buttons_group_box(self):
        buttons_group = QGroupBox()
        buttons_layout = QHBoxLayout()

        log_path_dialog_button = QPushButton('set path')
        log_path_dialog_button.clicked.connect(self.set_path)
        buttons_layout.addWidget(log_path_dialog_button)

        log_path_save_button = QPushButton('save path')
        log_path_save_button.clicked.connect(self.save_path)
        buttons_layout.addWidget(log_path_save_button)

        subdir_reset_button = QPushButton('reset subdir')
        subdir_reset_button.clicked.connect(self.reset_path)
        buttons_layout.addWidget(subdir_reset_button)

        buttons_group.setLayout(buttons_layout)
        return buttons_group

    def set_path(self):
        dirname = QFileDialog.getExistingDirectory(parent=self,
                                                   caption='Choose Logs dir',
                                                   directory=self._path_service.get_log_path() or '.')
        if dirname:
            self._path_service.set_log_path(dirname)
            self.log_path_value_label.setText(dirname)

    def save_path(self):
        if self._path_service.save_log_path():
            print("Great success. Everything is saved.")
            return
        print("No success. None will be saved.")

    def reset_path(self):
        if self._path_service.set_subdir():
            self.subdir_value_label.setText(self._path_service.get_subdir_name())


class ValueBox(QGroupBox):
    """
    I want a box that displays a value and a title. Gundarnit.
    Title is thought of as immutable here, value should be trivial to change/link.

    #####################################
    #title                              #
    #####################################
    #                                   #
    # VALUE                             #
    #                                   #
    #####################################
    """
    def __init__(self, parent=None, title=None):
        super().__init__(parent=parent, title=title)
        # self.

