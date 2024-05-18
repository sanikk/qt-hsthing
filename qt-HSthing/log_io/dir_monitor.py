from watchdog.observers import Observer
from pathlib import Path

from log_io.log_reader import LogReader

from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication


class DirMonitor(QObject):
    """
    paras olisi varmaan hoitaa tämä eventeillä. Joko event_handleri joka tuottaa qeventtejä,
    tai sitten jos sais määritettyä suoraan mitä eventtejä toi watchdog luo.

    Jos luodaan log_servicessä event_handler instanssi ja linkitetään se siellä.
    log_service -> dir_monitor -> observer.schedule(event_handler=event_handler)
    QObject.__init__ ja on signaalit.
    """

    new_content = pyqtSignal(str)

    def __init__(self, directory_path=None, filenames=None, event_handler=None):
        super().__init__()
        self.observer = ObserverWrapper()
        self.directory_path = directory_path
        self.filenames = filenames
        self.event_handler = event_handler

    def run(self):
        print(f"dir_mon {self.event_handler=}")
        print(f"dir_mon {self.directory_path=}")
        self.observer.schedule(
            event_handler=self.event_handler,
            path=self.directory_path
        )
        # print(f"{self.observer.get_watches()}")
        self.observer.start()

    def stop_reading(self):
        self.observer.stop()
        self.observer.unschedule_all()
        self.deleteLater()

    @pyqtSlot(str)
    def signal_new_content(self, filepath):
        print(f"dir_monitor handler func received: {filepath=}")


class ObserverWrapper(Observer):
    def __init__(self, **kwargs) -> None:
        super().__init__(*kwargs)

    def get_watches(self):
        return self._watches
