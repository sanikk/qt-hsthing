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
        self.observer = Observer()
        self.directory_path = directory_path
        self.filenames = filenames
        self.event_handler = event_handler

    def run(self):
        self.observer.schedule(
            event_handler=self.event_handler,
            path=self.directory_path
        )

    def stop_reading(self):
        self.observer.stop()
        self.observer.unschedule_all()
        self.deleteLater()

    @pyqtSlot(str)
    def signal_new_content(self, filepath):
        print(f"dir_monitor handler func received: {filepath=}")
        # logfile, content = self.log_reader.read_log(filepath)
        # print(f"handle_new_content {logfile=}")
        # print(f"handle_new_content {content=}")
        # if content:
        #     for line in content:
        #         self.new_content.emit(line)


if __name__ == '__main__':
    app = QApplication([])
    sub_dir_path = Path()
    filenames = ['Achievements.log', 'Gameplay.log', 'Power.log']
    log_reader = LogReader(sub_dir_path=sub_dir_path, filenames=filenames)
    monitor = DirMonitor(directory_path=sub_dir_path, filenames=filenames)
    monitor.run()
    app.exec()
