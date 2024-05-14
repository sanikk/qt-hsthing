from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject, QThread
from pathlib import Path
from log_io.log_reader_worker import LogReaderWorker


class LogService(QObject):
    start_monitor = pyqtSignal()
    stop_monitor = pyqtSignal()
    # add_path = pyqtSignal(str)

    def __init__(self, subdir_path=None):
        super().__init__()
        print('main running in:', QThread.currentThread())

        self.files_to_watch = []
        self._make_filepaths(subdir_path)

        self.worker = LogReaderWorker(paths=self.files_to_watch)
        self.worker.connect(self)
        self.thread = QThread()

        self.worker.monitor_started.connect(self.onWorkerStarted)
        self.worker.monitor_stopped.connect(self.onWorkerStopped)
        self.worker.text_ready.connect(self.onTextReady)

        self.worker.moveToThread(self.thread)
        self.thread.start()

    def _make_filepaths(self, subdir_path=None):
        if not subdir_path:
            return
        filenames = ['Achievements.log', 'Gameplay.log', 'Power.log']
        self.files_to_watch = [Path(subdir_path, file) for file in filenames]

    # LogReaderWorker stuff
    def start_worker(self, subdir_path=None):
        if subdir_path:
            self._make_filepaths(subdir_path)

        print("main: sending start signal")
        self.start_monitor.emit()

    def stop_worker(self):
        print("main: sending stop signal")
        self.stop_monitor.emit()

    @pyqtSlot()
    def onWorkerStarted(self):
        print("main: worker has started in another thread")

    @pyqtSlot()
    def onWorkerStopped(self):
        print("main: everything done, cleaning up")
        self.thread.quit()
        self.thread.wait()
        self.close()

    @pyqtSlot(str)
    def onTextReady(self, text):
        print(f"main: received text {text}")
