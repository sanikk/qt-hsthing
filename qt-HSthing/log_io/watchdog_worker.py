from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# from log_io.log_reader import LogReader


class WatchdogWorker(QObject):
    """
    tän ei oikeasti tarvitse olla missään qthreadissa, koitin vain tehdä suoraan vaihdettavaa moduulia
    """

    monitor_started = pyqtSignal()
    monitor_stopped = pyqtSignal()
    text_ready = pyqtSignal(str)

    def __init__(self, sub_dir_path: str = None):
        super().__init__()
        self.filenames = ['Achievements.log', 'Gameplay.log', 'Power.log']
        self.sub_dir_path = sub_dir_path

        self.observer = Observer()
        # self.log_reader = LogReader(sub_dir_path=sub_dir_path)

    def connect(self, connectee: QObject = None):
        if not connectee:
            return
        connectee.start_monitor.connect(self.start_monitor)
        connectee.stop_monitor.connect(self.stop_monitor)
        connectee.add_path.connect(self.add_path)

    @pyqtSlot()
    def start_monitor(self):
        if not self.sub_dir_path:
            return
        print("start_monitor doing good")
        self.start_observer()

        self.monitor_started.emit()

    def start_observer(self):
        self.observer.unschedule_all()
        self.observer.schedule(
            event_handler=Handler(filenames=self.filenames),
            path=self.sub_dir_path
        )
        if not self.observer.is_alive():
            self.observer.start()

    @pyqtSlot()
    def stop_monitor(self):
        self.observer.unschedule_all()
        self.observer.stop()
        self.deleteLater()
        self.monitor_stopped.emit()

    @pyqtSlot(str)
    def add_path(self, new_path: str):
        self.sub_dir_path = new_path
        self.start_observer()


class Handler(FileSystemEventHandler):
    def __init__(self, filenames=None):
        super().__init__()

        self.filenames = filenames

    def on_modified(self, event) -> None:
        """

        :param event: full path as str
        :return:
        """
        if event.is_directory:
            return None
        filename = event.src_path.split('/')[-1]
        if filename in self.filenames:
            print("a watched file was modified")
        # print(f"handler {filename=}")
        # print(f"{event=}")
        # path, content = self.log_reader.read_log(event.src_path)
        # if content:
            # this should be made sync/async and threadsafe
            # self.log_service.add_content(content=content)
            # print(content)


if __name__ == '__main__':
    import PyQt6.QtWidgets as QtW
    import PyQt6.QtCore as QtC

    app = QtW.QApplication([])

    worker = WatchdogWorker(sub_dir_path='/home/karpo/hd/SteamLibrary/steamapps/common/HS/Hearthstone/Logs/Hearthstone_2024_05_15_11_14_22/')
    cunt = QtW.QMainWindow()
    button = QtW.QPushButton('Push me!')
    cunt.setCentralWidget(button)
    button.clicked.connect(worker.start_monitor)
    cunt.show()

    app.exec()
    exit()
