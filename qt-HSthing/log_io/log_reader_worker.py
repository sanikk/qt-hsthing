from PyQt6.QtCore import pyqtSignal, QObject, QFileSystemWatcher, QThread, pyqtSlot


class LogReaderWorker(QObject):
    """
    ach. tää varaa nyt kuitenkin noi tiedostot.
    """
    monitor_started = pyqtSignal()
    monitor_stopped = pyqtSignal()
    text_ready = pyqtSignal(str)

    def __init__(self, sub_dir_path: str = None):
        super().__init__()
        self.monitor = None
        self.path = sub_dir_path
        self.filenames = ['Achievements.log', 'Gameplay.log', 'Power.log']

    def connect(self, connectee: QObject):
        connectee.start_monitor.connect(self.start_monitor)
        connectee.stop_monitor.connect(self.stop_monitor)
        connectee.add_path.connect(self.add_path)

    @pyqtSlot()
    def start_monitor(self):
        if not self.monitor:
            print('Worker started in:', QThread.currentThread())
            self.monitor = QFileSystemWatcher([self.path])
        if self.path:
            print(f"{self.monitor.directories()=}")
            self.monitor_started.emit()
            self.monitor.directoryChanged.connect(self.check_file)
            self.monitor.fileChanged.connect(self.check_file)
        else:
            print("worker: no path set")

    @pyqtSlot(str)
    def check_file(self, path: str):
        if path not in self.monitor.directories():
            # file was likely deleted and recreated
            # ok i dont know why this would happen with a dir
            self.monitor.addPath(path)
            self.text_ready.emit(f"worker: {path} was recreated?")
        else:
            self.text_ready.emit(f"worker: {path} was changed.")

    @pyqtSlot()
    def stop_monitor(self):
        print("worker stopping monitor")
        if self.monitor:
            self.monitor.removePaths(self.monitor.directories())
        self.deleteLater()
        self.monitor_stopped.emit()

    @pyqtSlot(str)
    def add_path(self, new_path):
        if self.path and self.monitor:
            self.monitor.removePaths([self.path])
        if new_path:
            self.path = new_path
            print(f"worker added path {new_path}")

