from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject

from log_io.dir_monitor import DirMonitor, QFileSystemEventHandler
from log_io.log_reader import LogReader


class LogService(QObject):

    content_ready = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.dir_monitor = None
        self.log_reader = None
        self.filenames = ['Achievements.log', 'Gameplay.log', 'Power.log']

    def start_reading(self, subdir_path: str = None):
        event_handler = QFileSystemEventHandler(filenames=self.filenames)
        event_handler.path_has_content.connect(self.testeri)
        if not subdir_path:
            return
        self.log_reader = LogReader(subdir_path)
        self.dir_monitor = DirMonitor(subdir_path, event_handler=event_handler)
        self.dir_monitor.run()

    def stop_reading(self):
        if self.dir_monitor:
            self.dir_monitor.stop_reading()
        self.deleteLater()

    # TODO rm this, just checking for connection
    @pyqtSlot(str)
    def testeri(self, filepath: str):
        print(f"log_service {filepath=}")


if __name__ == '__main__':
    import PyQt6.QtCore as QtC
    import PyQt6.QtWidgets as QtW
    app = QtW.QApplication([])
