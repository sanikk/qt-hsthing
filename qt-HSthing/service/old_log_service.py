from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject, QThread
from pathlib import Path
from log_io.log_reader_worker import LogReaderWorker
from log_io.watchdog_worker import WatchdogWorker


class LogService(QObject):
    start_monitor = pyqtSignal()
    stop_monitor = pyqtSignal()
    add_path = pyqtSignal(str)

    def __init__(self, subdir_path: str = None):
        super().__init__()

        # self.worker = LogReaderWorker(sub_dir_path=subdir_path)
        self.worker = WatchdogWorker()
        self.worker.connect(self)
        self.thread = QThread()

        self.worker.monitor_started.connect(self.onWorkerStarted)
        self.worker.monitor_stopped.connect(self.onWorkerStopped)
        self.worker.text_ready.connect(self.onTextReady)

        self.worker.moveToThread(self.thread)
        self.thread.start()

    # LogReaderWorker stuff
    def start_worker(self, subdir_path=None):
        if subdir_path:
            self.add_path.emit(subdir_path)
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

    @pyqtSlot(str)
    def onTextReady(self, text):
        print(f"main: received text {text}")


if __name__=='__main__':
    import PyQt6.QtCore as QtC
    import PyQt6.QtWidgets as QtW
    app = QtW.QApplication([])
