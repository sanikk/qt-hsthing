from PyQt6.QtCore import pyqtSignal, QObject, QFileSystemWatcher, QThread, pyqtSlot


class LogReaderWorker(QObject):
    monitor_started = pyqtSignal()
    monitor_stopped = pyqtSignal()
    text_ready = pyqtSignal(str)

    def __init__(self, paths: set[str] = None):
        super().__init__()
        self.monitor = None
        self.paths = paths or set()

    def connect(self, connectee: QObject):
        connectee.start_monitor.connect(self.start_monitor)
        connectee.stop_monitor.connect(self.stop_monitor)
        connectee.add_path.connect(self.add_path)

    @pyqtSlot()
    def start_monitor(self):
        if self.paths:
            print('Worker started in:', QThread.currentThread())
            self.monitor = QFileSystemWatcher(self.paths)
            print(f"{self.monitor.files()=}")
            self.monitor_started.emit()
            self.monitor.fileChanged.connect(self.check_file)
        else:
            print("worker: failed to start")

    @pyqtSlot(str)
    def check_file(self, path: str):
        print("worker: check_file fired")
        if path not in self.monitor.files():
            # file was likely deleted and recreated
            self.monitor.addPath(path)
            self.text_ready.emit(f"worker: {path} was recreated.")
        else:
            self.text_ready.emit(f"worker: {path} was changed.")

    @pyqtSlot()
    def stop_monitor(self):
        print("worker stop signal received")
        if self.monitor:
            self.monitor.removePaths(self.paths)
        self.deleteLater()
        self.monitor_stopped.emit()

    @pyqtSlot(str)
    def add_path(self, new_path):
        if not self.paths:
            self.paths = set()
        if new_path:
            self.paths.add(new_path)

