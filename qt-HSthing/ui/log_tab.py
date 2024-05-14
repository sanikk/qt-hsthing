from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTextEdit, QWidget


class LogTab(QTextEdit):
    def __init__(self, parent: QWidget = None, log_service=None):
        super().__init__(parent=parent)
        self._log_service = log_service

        self.setReadOnly(True)

    def start_updater(self, delay=50):
        self._ui.after(delay, self.after_callback)

    def after_callback(self):
        content = self._log_service.fetch()
        if content:
            print(f"ui.after_callback {content=}")
            self.output_box.insert('end', *content)
        self._ui.after(10, self.after_callback)
        self.frame.update_idletasks()

