from pathlib import Path
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject

from io_functionality.dir_monitor import DirMonitor
from io_functionality.fs_utils import cleanup
from io_functionality.log_reader import LogReader
from io_functionality.qfilesystemeventhandler import QFileSystemEventHandler
from service.log_processor import LogProcessor


class LogService(QObject):
    content_ready = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.dir_monitor = None
        self.log_reader = None
        self.filenames = ['Achievements.log', 'Gameplay.log', 'Power.log']
        # convenience variable to store path with pyqtSlot-connected setter
        self.fetch_path = None
        self.event_handler = None
        self.log_processor = LogProcessor()

    def start_reading(self, subdir_path: str = None):
        if not subdir_path:
            return
        # we make this here for ez connects
        self.event_handler = QFileSystemEventHandler(filenames=self.filenames)
        self.event_handler.path_has_content.connect(self.set_fetch_path)
        self.event_handler.path_has_content.connect(self.content_ready)
        *log_path, subdir = Path(subdir_path).parts
        log_path = str(Path(*log_path))
        cleanup(log_path, subdir)
        self.log_reader = LogReader(subdir_path)
        self.dir_monitor = DirMonitor(subdir_path, event_handler=self.event_handler)
        self.dir_monitor.run()

    def stop_reading(self):
        if self.dir_monitor:
            self.dir_monitor.stop_reading()
        self.deleteLater()

    @pyqtSlot(str)
    def set_fetch_path(self, path: str):
        self.fetch_path = path

    def fetch(self):
        # saved here for nostalgic reasons, nvm
        # return 'supreme data'
        self.event_handler.blockSignals(True)
        data = self.log_reader.read_log_file(self.fetch_path)
        self.event_handler.blockSignals(False)
        with open('raw_input.txt', 'a') as f:
            f.write(data)
        filtered = [self.log_processor.rough_cut(line) for line in data.split("\n")]
        filtered = [self.log_processor.match_case_version(line) for line in data.split("\n")]
        cleaner = [part for part in filtered if part]
        joined = "\n".join(cleaner)
        with open('output.txt', 'a') as f:
            f.write(joined)

        return filtered
