from pathlib import Path
from queue import Queue, Empty
from PyQt6.QtCore import QThread, QObject, QFileSystemWatcher, pyqtSlot


class Worker(QFileSystemWatcher):
    def __init__(self):
        super().__init__()
        self.fileChanged.connect(self.check_file)

    @pyqtSlot(str)
    def check_file(self, path: str):
        if path not in self.files():
            # file was likely deleted and recreated
            self.addPath(path)


class LogService(QObject):
    def __init__(self):
        super().__init__()
        self.watcherThread = None
        self.watcher = None
        self.last_read = {}

    def start_monitor(self, subdir_path=None):
        if not subdir_path:
            return
        # let pathlib build urls, and str them out
        filelist = [str(Path(subdir_path, a)) for a in ['Achievements.log', 'Gameplay.log', 'Power.log'] if Path(subdir_path, a).exists()]
        self.watcherThread = QThread()
        self.watcher = QFileSystemWatcher()
        self.watcher.moveToThread(self.watcherThread)
        self.watcherThread.finished.connect(self.watcherThread.deleteLater)
        # self.wat
        # self.watcher.fileChanged.connect(self.check_file)
        # self.watcherThread.start()
        # self.watcher.addPaths(filelist)


